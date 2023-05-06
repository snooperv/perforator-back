from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import peers

"""
    Тестовые роуты для тестирования пиров.
    Все роуты возвращают JSON
"""


def peers_demo(request):
    return render(request,
                  'test/peers_demo.html')


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


@api_view(['GET'])
def get_where_user_id_is_peer(request):
    return Response(data=peers.get_where_user_id_is_peer(request, request.GET['id']), status=200)


@api_view(['GET'])
def get_user_peers(request):
    return Response(data=peers.get_user_peers(request, request.GET['id']), status=200)


@api_view(['POST'])
def delete_user_peers(request):
    return Response(data=peers.delete_user_peers(request, request.GET['id']), status=200)


@api_view(['POST'])
def save_user_peers(request):
    return Response(data=peers.save_user_peers(request, request.GET['id']), status=200)


@api_view(['POST'])
def approve_user(request):
    return Response(data=peers.approve_user(request, request.GET['id']), status=200)


@api_view(['GET'])
def get_user_rating_by_id(request):
    return Response(data=peers.get_user_rating(request, request.GET['id']), status=200)