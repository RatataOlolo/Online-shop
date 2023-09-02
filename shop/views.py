import json

from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from django.http import JsonResponse

from .forms import RegisterUserForm, LoginUserForm, OrderForm
from .models import Product, Order, OrderItem
from .utils import cookieCart, cartData, DataMixin, menu


class ShopHome(DataMixin, ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Головна сторінка")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Product.objects.filter(is_published=True)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')


class ShowProduct(DataMixin, DetailView):
    model = Product
    template_name = 'shop/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['product'])
        return dict(list(context.items()) + list(c_def.items()))


class ShopCategory(DataMixin, ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категорія - ' + str(context['products'][0].cat),
                                      cat_selected=context['products'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


class SearchResultsView(DataMixin, ListView):
    model = Product
    template_name = 'shop/search_results.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Результат пошуку")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(title__icontains=query)
        return object_list


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Реєстрація")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизація")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserProfileView(DetailView):
    model = User
    template_name = 'shop/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer = self.request.user
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

        context.update({
            'menu': menu,
            'title': 'Профіль',
            'h1': 'Профіль',
            'items': items,
            'order': order,
            'cartItems': cartItems,
        })
        return context


def contacts(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {
        'menu': menu,
        'title': 'Наші контакти',
        'h1': 'Наші контакти',
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'shop/contacts.html', context)


def delivery(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {
        'menu': menu,
        'title': 'Доставка та оплата',
        'h1': 'Доставка та оплата',
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'shop/delivery.html', context)


def stickers_print(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {
        'menu': menu,
        'title': 'Друк власних стікерів',
        'h1': 'Друк власних стікерів',
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'shop/stickers_print.html', context)


def car_print(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {
        'menu': menu,
        'title': 'Написи на авто',
        'h1': 'Написи на авто',
        'h1': 'Написи на авто',
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'shop/car_print.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {
        'menu': menu,
        'title': 'Кошик',
        'h1': 'Кошик',
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'shop/cart.html', context)


def orderresult(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {
        'menu': menu,
        'title': 'Замовлення успішне',
        'h1': 'Ваше замовлення прийнято!',
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'shop/order_result.html', context)


def checkout(request):
    data = cartData(request)
    ordernum = data['order']
    items = data['items']
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        initial_dict = {
            "customer": customer,
            "order": ordernum,
        }
        form = OrderForm(request.POST or None, initial=initial_dict)
        if request.method == 'POST' or request.method == 'None':
            if form.is_valid():
                for item in items:
                    product = Product.objects.get(id=item.product_id)
                    orderItem = OrderItem.objects.create(
                        product=product,
                        order=order,
                        quantity=(item.quantity if item.quantity > 0 else -1 * item.quantity),
                    )
                    orderItem.save()
                form.save()
        order.complete = True
        order.save()
        return redirect('order_result')
    else:
        return redirect('login')


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if orderItem.quantity >= 1:
            orderItem.quantity += 1
        else:
            orderItem.quantity = 1
    elif action == 'remove':
        orderItem.quantity -= 1
        if orderItem.quantity <= 0:
            orderItem.delete()
    if action == 'delete':
        orderItem.quantity = 0
        if orderItem.quantity <= 0:
            orderItem.delete()

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
