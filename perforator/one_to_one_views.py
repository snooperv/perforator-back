from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import one_to_one


@api_view(['POST'])
def get_common_notes(request):
    return Response(data=one_to_one.getCommonNotes(request), status=200)


@api_view(['POST'])
def update_common_notes(request):
    return Response(data=one_to_one.updateCommonNotes(request), status=200)


@api_view(['POST'])
def get_private_notes(request):
    return Response(data=one_to_one.getPrivateNotes(request), status=200)


@api_view(['POST'])
def update_private_notes(request):
    return Response(data=one_to_one.updatePrivateNotes(request), status=200)
