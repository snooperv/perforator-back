from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class RegistrationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput())
    phone = forms.CharField(widget=forms.TextInput())
    sbis = forms.CharField(widget=forms.URLInput())
    password = forms.CharField(widget=forms.PasswordInput())
    photo = forms.ImageField(widget=forms.FileInput())


class UpdateProfile(forms.Form):
    name = forms.CharField(widget=forms.TextInput())
    phone = forms.CharField(widget=forms.TextInput())
    sbis = forms.CharField(widget=forms.TextInput())


class SelfReviewForm(forms.Form):
    input_1 = forms.CharField(widget=forms.TextInput())
    input_2 = forms.CharField(widget=forms.TextInput())
    successes_1 = forms.CharField(widget=forms.TextInput())
    successes_2 = forms.CharField(widget=forms.TextInput())
    plans_1 = forms.CharField(widget=forms.TextInput())
    plans_2 = forms.CharField(widget=forms.TextInput())
