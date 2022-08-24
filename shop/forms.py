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



class OrderForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['customer', 'order', 'firstname', 'lastname', 'delivery', 'post_department', 'city', 'region', 'phoneNumber', 'comment', 'payment']
        exclude = ['date_added']
        widgets = {'customer': forms.HiddenInput(), 'order':forms.HiddenInput()}
