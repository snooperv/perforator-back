from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.SelfReviewByUserView.as_view(), name='index'),
    url(r'^registration/$', views.registration, name='registration'),
]
