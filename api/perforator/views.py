from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .form import RegistrationForm
from django.contrib.auth.models import User
from .models import SelfReview, PUser
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    num_self = SelfReview.objects.all().count()
    return render(request,
                  'index.html',
                  context={'num_self': num_self})


class SelfReviewByUserView(LoginRequiredMixin, generic.ListView):
    model = SelfReview

    def get_queryset(self):
        return SelfReview.objects.filter(self_review=self.request.user)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = PUser.objects.create_user(form.cleaned_data['phone'], '', form.cleaned_data['password'])
            user.phone = form.cleaned_data['phone']
            user.first_name = form.cleaned_data['name']
            user.sbis = form.cleaned_data['sbis']
            user.save()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegistrationForm(initial={'name': "", 'phone': "", 'sbis': "", 'password': ""})
    return render(request, 'perforator/registration.html', {'form': form})
