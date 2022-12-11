from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import general


@api_view(['GET'])
def my_profile(request):
    return Response(data=general.my_profile(request), status=200)


@api_view(['POST'])
def login_token(request):
    return Response(data=general.login(request), status=200)