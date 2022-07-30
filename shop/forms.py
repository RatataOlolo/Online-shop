from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'input'}) )
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'input'}) )
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'input'}) )
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'input'}) )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput() )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput() )

# class OrderForm(forms.Form):
#     NP = 'Нова пошта'
#     UP = 'Укрпошта'
#     S = 'Самовивіз, м.Полтава'
#     PP = 'Передплата на карту ПриватБанк'
#     NlP = 'Готівка при отриманні (тiльки для замовлень вiд 100 грн.)'
#     delivery_type = [
#         (NP, 'Нова пошта'),
#         (UP, 'Укрпошта'),
#     ]
#     payment_type = [
#         (PP, 'Передплата на карту ПриватБанк'),
#         (NlP, 'Готівка при отриманні (тiльки для замовлень вiд 100 грн.)'),
#     ]
#     firstname = forms.CharField(max_length=128, required=True, label='Ім\'я')
#     lastname = forms.CharField(max_length=128 ,required=True, label='Прізвище')
#     delivery = forms.ChoiceField(choices=delivery_type, label='Оберіть спосіб доставки')
#     post_department = forms.IntegerField(label='Номер відділення')
#     city = forms.CharField(required=True, label='Населений пункт')
#     region = forms.CharField(required=False, label='Область (необов\'язково)')
#     # phoneNumber = forms.RegexField(regex=r'\0(\d{9})', max_length=10, label='Контактний номер в форматі 0ххххххххх')
#     phoneNumber = forms.IntegerField(label='Контактний номер в форматі 0ххххххххх')
#     comment = forms.CharField(max_length=300, required=False, label='Коментар до замовлення')
#     payment = forms.ChoiceField(choices=payment_type, label='Спосіб оплати')

class OrderForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['customer', 'order', 'firstname', 'lastname', 'delivery', 'post_department', 'city', 'region', 'phoneNumber', 'comment', 'payment']
        exclude = ['date_added']
        widgets = {'customer': forms.HiddenInput(), 'order':forms.HiddenInput()}