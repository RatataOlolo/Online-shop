from django.contrib.auth.models import User
from django.db.models import Count
import json

from shop.models import Category, Order, Product, OrderItem

menu = [{'title': 'Магазин', 'url_name': 'home'},
        {'title': 'Доставка та оплата', 'url_name': 'delivery'},
        {'title': 'Контакти', 'url_name': 'contacts'},
        {'title': 'Друк власних стікерів', 'url_name': 'stickers_print'},
        {'title': 'Написи на авто', 'url_name': 'car_print'},
        ]


class DataMixin:
    paginate_by = 12

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('product'))

        if self.request.user.is_authenticated:
            customer = self.request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items

        else:
            cookieData = cookieCart(self.request)
            cartItems = cookieData['cartItems']
            order = cookieData['order']
            items = cookieData['items']

        context['menu'] = menu
        context['cats'] = cats
        context['items'] = items
        context['order'] = order
        context['cartItems'] = cartItems

        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context


def cookieCart(request):
    # Create empty cart for now for non-logged in user
    cart = json.loads(request.COOKIES['cart'])

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        if (cart[i]['quantity'] > 0):
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'id': product.id,
                'product': {'id': product.id, 'name': product.title, 'price': product.price,
                            'photo': product.photo}, 'quantity': cart[i]['quantity'], 'get_total': total,
            }
            items.append(item)

            order['shipping'] = True

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        return {'cartItems': cartItems, 'order': order, 'items': items, 'customer': customer}
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        return {'cookieData': cookieData, 'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    first_name = data['form']['firstname']
    last_name = data['form']['lastname']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, _ = User.objects.get_or_create(firstname=first_name, last_name=last_name)
    customer.firstname = first_name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        OrderItem.objects.create(
            product=product,
            order=order,
            quantity=(item['quantity'] if item['quantity'] > 0 else -1 * item['quantity']),
        )
    return customer, order
