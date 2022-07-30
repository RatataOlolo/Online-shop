from django import template
from shop.models import *

register = template.Library() #ex of class Library

# @register.simple_tag()
# def get_categories():
#     return Category.objects.all() #creating of simple tag. It will be func that returns all categories.
#
# @register.simple_tag(name='getproducts')
# def get_products():
#     return Product.objects.filter(is_published=True)
#
#
# @register.simple_tag(name='getcats')
# def get_categories():
#     return Category.objects.all()

# @register.inclusion_tag('stickersplt/list_categories.html') #включающий тег
# def show_categories():
#     cats = Category.objects.all()
#     return {'cats': cats}

# @register.simple_tag(name='pr_count')
# def product_count():
#     p_count = Product__set.filter(c).count()
#     return p_count