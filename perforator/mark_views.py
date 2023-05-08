from rest_framework.response import Response
from rest_framework.decorators import api_view
from perforator import questions, ratings


@api_view(['POST'])
def create_questionary(request):
    return Response(data=questions.questionary_create(request), status=200)


@api_view(['POST'])
def update_questionary(request):
    return Response(data=questions.questionary_update(request), status=200)


@api_view(['POST'])
def get_questionary(request):
    return Response(data=questions.questionary_get(request), status=200)


@api_view(['POST'])
def get_user_rating(request):
    return Response(data=ratings.user_rating(request), status=200)
