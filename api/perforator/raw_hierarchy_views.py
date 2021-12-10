from rest_framework.response import Response
from rest_framework.decorators import api_view
from .hierarchy import *
from django.shortcuts import render
from django.http import HttpRequest


@api_view(['GET'])
def get_profile_manager(request):
    return Response(data=get_manager(request), status=200)


@api_view(['GET'])
def get_profile_team(request):
    return Response(data=get_team(request), status=200)


@api_view(['GET'])
def get_full_hierarchy_tree(request):
    return Response(data=get_full_tree(), status=200)