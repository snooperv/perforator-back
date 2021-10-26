import base64
from rest_framework.decorators import api_view
from .models import User, Profile
from .crypto import gen_token
from rest_framework.response import Response


@api_view(['GET'])
def get_current_user(request):
    """
        Получить данные пользователя, который авторизовался. Чтобы получить данные любого пользователя,
        используйте get_user_info
    """
    if 'token' not in request.session.keys():
        return Response(data={'message': 'Вы не авторизовались'}, status=400)
    token = request.session['token']
    user = User.objects.filter(token=token)[0]
    return Response(data={'id': user.id,
                          'username': user.username,
                          'phone': user.phone,
                          'sbis': user.sbis}, status=200)


@api_view(['GET'])
def get_user_info(request):
    """
        Получить данные любого пользователя по номеру телефона (пока только по номеру).
        Чтобы получить данные авторизованного пользователя, используйте get_current_user
    """
    pass


@api_view(['GET'])
def get_profile_info(request):
    """
        Селянин 26.10:
        Метод для чтения профиля по id. Используется для получения данных для личной
        странички пользователя.
    """
    if 'token' not in request.session.keys():
        return Response(data={'message': 'Вы не авторизовались'}, status=400)
    token = request.session['token']
    user = User.objects.filter(token=token)[0]
    profile = user.profile
    with open(f'../../files/{profile.photo}.jpg', "rb") as image_file:
        photo_data = base64.b64encode(image_file.read()).decode('utf-8')
    return Response(data={'id': user.id,
                          'username': user.username,
                          'phone': user.phone,
                          'sbis': user.sbis,
                          'photo': photo_data
                          }, status=200)



@api_view(['GET'])
def get_profile_info(request):
    pass

