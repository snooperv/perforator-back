from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': 'Имя и фамилия'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn second', 'placeholder': "Номер телефона (+79...)"}))
    sbis = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn third', 'placeholder': "Ссылка на профиль СБИС (http://...)"}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'fadeIn third', 'placeholder': "Пароль"}))

