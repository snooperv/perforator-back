from django.http import HttpResponse
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from models import Profile

def basicView(request):
    html = "<html><body>Hello!</body></html>"
    return HttpResponse(html)

def registerUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            login(request, user)
            profile = Profile(user=user, phone=request.REQUEST.get('phone', None))

# Можно вставлять и настоящие HTML-файлы, посмотрите в Django
