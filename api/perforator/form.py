from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import PeerReviews


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


class RateForm(forms.Form):
    """
        Форма оценки пользователя в разделе 'Я оцениваю'
    """
    RATES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]
    deadlines = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': 512}))
    approaches = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': 512}))
    teamwork = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': 512}))
    practices = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': 512}))
    experience = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': 512}))
    adaptation = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'maxlength': 512}))
    rates_deadlines = forms.ChoiceField(choices=RATES, widget=forms.RadioSelect)
    rates_approaches = forms.ChoiceField(choices=RATES, widget=forms.RadioSelect)
    rates_teamwork = forms.ChoiceField(choices=RATES, widget=forms.RadioSelect)
    rates_practices = forms.ChoiceField(choices=RATES, widget=forms.RadioSelect)
    rates_experience = forms.ChoiceField(choices=RATES, widget=forms.RadioSelect)
    rates_adaptation = forms.ChoiceField(choices=RATES, widget=forms.RadioSelect)

    def __dict__(self):
        return self.cleaned_data
