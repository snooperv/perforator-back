from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import general


@api_view(['GET'])
def my_profile(request):
    return Response(data=general.my_profile(request), status=200)


@api_view(['POST'])
def login_token(request):
    response_data = general.login(request)
    if response_data['status'] == 'ok':
        token_b = response_data['token_b']
        response_data['token_b'] = ''
        response = Response(data=response_data, status=200)
        response.set_cookie(key='token_b', value=token_b, max_age=604800, secure=True, httponly=True, samesite="None")
    else:
        response = Response(data=response_data, status=200)
    return response


@api_view(['POST'])
def refresh_token(request):
    return Response(data=general.refresh_token(request), status=200)


@api_view(['GET'])
def get_irate_list(request):
    return Response(data=general.irate_list(request), status=200)


@api_view(['POST'])
def save_process_rate(request):
    return Response(data=general.processRate(request), status=200)


@api_view(['POST'])
def begin_next_stage(request):
    return Response(data=general.next_stage(request), status=200)


@api_view(['GET'])
def get_pr_status(request):
    return Response(data=general.pr_status(request), status=200)


@api_view(['GET'])
def get_pr_list(request):
    return Response(data=general.pr_list(request), status=200)


@api_view(['POST'])
def begin_performance_review(request):
    return Response(data=general.begin_perforator(request), status=200)


@api_view(['POST'])
def close_performance_review(request):
    return Response(data=general.close_perforator(request), status=200)


@api_view(['POST'])
def pr_get_review(request):
    return Response(data=general.pr_review(request), status=200)


@api_view(['POST'])
def pr_get_common_notes(request):
    return Response(data=general.pr_common_notes(request), status=200)


@api_view(['POST'])
def pr_get_private_notes(request):
    return Response(data=general.pr_private_notes(request), status=200)


@api_view(['POST'])
def get_user_rating_by_id(request):
    return Response(data=general.pr_user_rating_by_id(request), status=200)
