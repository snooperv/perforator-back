from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View

from .form import *
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    num_self = SelfReview.objects.all().count()
    return render(request,
                  'main/index.html',
                  context={'num_self': num_self})


class I_Rate(LoginRequiredMixin, View):
    model = Grade

    @staticmethod
    def get(request):
        form = UpdateProfile(initial={'name': "", 'phone': "", 'sbis': ""})
        return render(request, 'main/mainfiles/i_rate.html', {'form': form})

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


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['phone'], '', form.cleaned_data['password'])
            user.profile.phone = form.cleaned_data['phone']
            user.first_name = form.cleaned_data['name']
            user.profile.sbis = form.cleaned_data['sbis']
            user.save()
            auto_login = authenticate(username=form.cleaned_data['phone'], password=form.cleaned_data['password'])
            login(request, auto_login)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegistrationForm(initial={'name': "", 'phone': "", 'sbis': "", 'password': ""})
    return render(request, 'registration/registration.html', {'form': form})






