from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render

from . import reviews
from .form import SelfReviewForm

"""
    Роуты для ревью (селф- и обычных).
    Созданы по аналогии с raw_peers_view.py
    Все роуты возвращают JSON
"""


def self_review(request):
    form = SelfReviewForm('self')
    review = reviews.get_self_review(request)
    return render(request,
                  'reviews/self_review.html', {'review_form': form, 'review': review})


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


@api_view(['GET'])
def get_empty_review_form(request):
    return Response(data=reviews.get_empty_review_form(request), status=200)


@api_view(['POST'])
def get_review(request):
    return Response(data=reviews.get_review(request), status=200)


@api_view(['POST'])
def save_review(request):
    return Response(data=reviews.save_review(request), status=200)


@api_view(['GET'])
def get_is_draft_status(request):
    return Response(data=reviews.is_draft(request, request.GET['id']), status=200)