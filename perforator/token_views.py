from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render

from . import tokens


@api_view(['POST'])
def login_token(request):
    return Response(data=tokens.login(request), status=200)
