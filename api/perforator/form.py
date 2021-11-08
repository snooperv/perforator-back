from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput())
    phone = forms.CharField(widget=forms.TextInput())
    sbis = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.TextInput())


class UpdateProfile(forms.Form):
    name = forms.CharField(widget=forms.TextInput())
    phone = forms.CharField(widget=forms.TextInput())
    sbis = forms.CharField(widget=forms.TextInput())


