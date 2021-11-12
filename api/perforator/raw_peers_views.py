from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View

from .form import *
from django.contrib.auth.models import User
from .models import SelfReview
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import peers

"""
    Тестовые роуты для тестирования пиров.
    Все роуты возвращают JSON
"""


@api_view(['GET'])
def get_all_peers(request):
    return Response(data=peers.get_all_peers(request), status=200)


@api_view(['GET'])
def get_all_current_user_peers(request):
    return Response(data=peers.get_all_current_user_peers(request), status=200)


@api_view(['POST'])
def delete_peers(request):
    return Response(data=peers.delete_peers(request), status=200)


@api_view(['POST'])
def save_peers(request):
    return Response(data=peers.save_peers(request), status=200)
