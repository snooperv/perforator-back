from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import reviews

"""
    Роуты для ревью (селф- и обычных).
    Созданы по аналогии с raw_peers_view.py
    Все роуты возвращают JSON
"""


@api_view(['GET'])
def get_self_review(request):
    return Response(data=reviews.get_self_review(request), status=200)


@api_view(['POST'])
def edit_self_review(request):
    return Response(data=reviews.edit_self_review(request), status=200)


@api_view(['GET'])
def get_empty_review_form(request):
    return Response(data=reviews.get_empty_review_form(request), status=200)


@api_view(['POST'])
def save_review(request):
    return Response(data=reviews.save_review(request), status=200)
