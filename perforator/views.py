from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from .form import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .ratings import *


class SelfReviewByUserView(LoginRequiredMixin, View):
    model = SelfReview

    @staticmethod
    def get(request):
        form = UpdateProfile(initial={'name': "", 'phone': "", 'sbis': ""})
        return render(request, 'main/mainfiles/self_review.html', {'form': form})

    @staticmethod
    def post(request):
        if request.method == 'POST':
            form = UpdateProfile(request.POST)

            if form.is_valid():
                user = User.objects.get(username=request.user.username)
                user.username = form.cleaned_data['phone']
                user.first_name = form.cleaned_data['name']
                user.profile.phone = form.cleaned_data['phone']
                user.profile.sbis = form.cleaned_data['sbis']
                user.save()
                return HttpResponseRedirect(reverse('index'))

    def get_queryset(self):
        return SelfReview.objects.filter(self_review=self.request.user)


class Employee(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        return render(request, 'main/mainfiles/addons/employee.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['phone'], '', form.cleaned_data['password'])
            user.profile.phone = form.cleaned_data['phone']
            user.first_name = form.cleaned_data['name']
            user.profile.sbis = form.cleaned_data['sbis']
            user.profile.company = Companies.objects.filter(id=form.cleaned_data['company']).first()
            photo = form.cleaned_data['photo']
            user.profile.photo = photo
            user.save()
        else:
            pass
    else:
        form = RegistrationForm(initial={'name': "", 'phone': "", 'sbis': "", 'password': ""})
    return render(request, 'registration/registration.html', {'form': form})
