from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import PeerReviews, PerformanceReview


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
    def __init__(self, formType):
        performance_review = PerformanceReview.objects.first()
        super().__init__()
        if formType == 'manager':
            categories = performance_review.manager_review_categories.all()
        elif formType == 'team':
            categories = performance_review.team_review_categories.all()
        elif formType == 'peers':
            categories = performance_review.peers_review_categories.all()
        else:
            categories = performance_review.self_review_categories.all()
        for category in categories:
            field_name = 'category_%s' % category.id
            self.fields[field_name] = forms.CharField(widget=forms.TextInput)
            self.initial[field_name] = ""

    def get_category_fields(self):
        for field_name in self.fields:
            if field_name.startswith('category_'):
                yield self[field_name]


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


class OneToOneForm(forms.Form):
    common = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'maxlength': 2048}), required=False)
    personal = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'maxlength': 2048}), required=False)

