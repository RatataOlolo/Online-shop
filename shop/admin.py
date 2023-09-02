from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.sessions.models import Session

from shop.models import Product, Category, Order, OrderItem, ShippingAddress


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'img_show', 'is_published', 'cat',
                    'in_stock')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_editable = ('is_published', 'in_stock')
    list_filter = ('is_published', 'time_create', 'in_stock')
    prepopulated_fields = {'slug': ('title',)}

    def img_show(self, obj):
        if obj.photo:
            return mark_safe("<img src = '{}' width=60 />".format(obj.photo.url))
        return None

    img_show.__name__ = 'IMG'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_orderd', 'complete')
    list_display_links = ('id', 'customer')
    search_fields = ('id', 'customer')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'quantity', 'date_added')
    list_display_links = ('id', 'order')
    search_fields = ('id', 'order')


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'firstname', 'lastname', 'delivery', 'city', 'payment', 'date_added')
    list_display_links = ('id', 'customer')
    search_fields = ('city', 'customer', 'date_added')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Session)
