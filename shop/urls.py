from django.urls import path, re_path

from .views import *
from . import views

urlpatterns = [
    path('', ShopHome.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('delivery/', delivery, name='delivery'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('product/<slug:product_slug>/', ShowProduct.as_view(), name='product'),
    path('category/<slug:cat_slug>/', ShopCategory.as_view(), name='category'),
    path('stickers_print/', stickers_print, name='stickers_print'),
    path('car_print/', car_print, name='car_print'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', updateItem, name='update_item'),
    path('search_results/', SearchResultsView.as_view(), name="search_results"),
    path('order_result/', orderresult, name="order_result"),
]
