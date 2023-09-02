from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Назва")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Опис")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Зображення")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Вартість')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Час створення")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Час зміни")
    is_published = models.BooleanField(default=True, verbose_name="Опубліковано")
    in_stock = models.BooleanField(default=True, verbose_name='Є в наявності')
    variant = models.BooleanField(default=False, null=True, blank=False)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категорія")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['id', 'title', 'time_create']


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name="Назва")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Зміст')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата останніх змін')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['id', 'time_create',
                    'title']


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['date_orderd']


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    class Meta:
        verbose_name = 'Товар в замовленні'
        verbose_name_plural = 'Товари в замовленні'
        ordering = ['date_added']


class ShippingAddress(models.Model):
    NP = 'Нова пошта'
    UP = 'Укрпошта'
    S = 'Самовивіз, м.Полтава'
    PP = 'Передплата на карту ПриватБанк'
    NlP = 'Готівка при отриманні (тiльки для замовлень вiд 100 грн.)'
    delivery_type = [
        (NP, 'Нова пошта'),
        (UP, 'Укрпошта'),
    ]
    payment_type = [
        (PP, 'Передплата на карту ПриватБанк'),
        (NlP, 'Готівка при отриманні (тiльки для замовлень вiд 100 грн.)'),
    ]

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Користувач')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Замовлення')
    firstname = models.CharField(max_length=128, null=True, verbose_name='Ім\'я')
    lastname = models.CharField(max_length=128, null=True, verbose_name='Прізвище')
    delivery = models.CharField(choices=delivery_type, max_length=128, null=True, verbose_name='Спосіб доставки')
    post_department = models.IntegerField(null=True, verbose_name='Номер відділення')
    city = models.CharField(max_length=128, null=True, verbose_name='Населений пункт')
    region = models.CharField(max_length=128, null=True, verbose_name='Область')
    phoneNumber = models.IntegerField(null=True, verbose_name='Контактний номер')
    comment = models.CharField(max_length=400, null=True, blank=True, verbose_name='Коментар до замовлення')
    payment = models.CharField(choices=payment_type, max_length=128, null=True, verbose_name='Спосіб оплати')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата замовлення')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Дані про замовлення'
        verbose_name_plural = 'Дані про замовлення'
        ordering = ['date_added']
