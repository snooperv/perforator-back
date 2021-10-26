from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls import include, url
from rest_framework import routers


app_name = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/base-auth/', include('rest_framework.urls')),
    path('api/v1/users/create', UserCreateView.as_view()),
    path('api/v1/users/all', UserListView.as_view()),
    path('api/v1/users/detail/<int:pk>', UserDetailView.as_view()),


]
