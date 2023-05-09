from rest_framework.response import Response
from rest_framework.decorators import api_view
from .hierarchy import *


@api_view(['GET'])
def get_profile_manager(request):
    return Response(data=get_manager(request), status=200)


@api_view(['POST'])
def post_become_manager(request):
    return Response(data=become_manager(request), status=200)


@api_view(['POST'])
def manager_status(request):
    return Response(data=get_manager_status(request), status=200)


@api_view(['POST'])
def team_update(request):
    return Response(data=update_team(request), status=200)


@api_view(['POST'])
def team_delete_user(request):
    return Response(data=delete_user_from_team(request), status=200)


@api_view(['GET'])
def get_profile_team(request):
    return Response(data=get_team(request), status=200)


@api_view(['GET'])
def all_users(request):
    return Response(data=get_all_users(request), status=200)