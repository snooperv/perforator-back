from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import reviews

"""
    Роуты для ревью (селф- и обычных).
    Созданы по аналогии с raw_peers_view.py
    Все роуты возвращают JSON
"""


@api_view(['POST'])
def pr_get_self_review(request):
    return Response(data=reviews.pr_self_review(request), status=200)


@api_view(['GET'])
def get_self_review(request):
    return Response(data=reviews.get_self_review(request), status=200)


@api_view(['GET'])
def get_self_review_by_id(request):
    return Response(data=reviews.get_self_review_by_id(request, request.GET['id']), status=200)


@api_view(['POST'])
def edit_self_review(request):
    return Response(data=reviews.edit_self_review(request), status=200)


@api_view(['POST'])
def get_review(request):
    return Response(data=reviews.get_review(request), status=200)


@api_view(['POST'])
def save_review(request):
    return Response(data=reviews.save_review(request), status=200)


@api_view(['GET'])
def get_is_draft_status(request):
    return Response(data=reviews.is_draft(request, request.GET['id']), status=200)