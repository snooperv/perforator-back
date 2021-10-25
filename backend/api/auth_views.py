from rest_framework.decorators import api_view
from .models import User
from .crypto import gen_token
from rest_framework.response import Response


@api_view(['POST'])
def auth(request):
    """
        Авторизация (точнее, здесь происходит регистрация) пользователя
        :return: токен, можно не сохранять на фронтенде, возвращается на всякий случай
    """
    users = User.objects.filter(phone=request.data['phone'])
    if len(users) > 0:
        return Response(data={'message': 'Пользователь с таким телефоном уже зарегистрирован'}, status=400)

    token = gen_token()
    u = User(username=request.data['username'], phone=request.data['phone'],
             sbis=request.data['sbis'], password=request.data['password'], token=token)
    u.save()
    result = {'token': token}
    request.session['token'] = token
    request.session.modified = True
    return Response(data=result, status=200)


@api_view(['GET'])
def login(request):
    """
        Логин пользователя
        :return: токен, можно не сохранять на фронтенде, возвращается на всякий случай
    """
    phone = request.data['phone']
    password = request.data['password']
    user = User.objects.filter(phone=phone, password=password)
    if len(user) == 0:
        return Response(data={'message': 'Неверный номер телефона или пароль'}, status=400)

    user = user[0]
    token = None
    if user.token != None:
        token = user.token
    else:
        token = gen_token()
        user.token = token
        user.save()
    result = {'token': token}
    request.session['token'] = token
    request.session.modified = True
    return Response(data=result, status=200)


@api_view(['GET'])
def logout(request):
    """
        Выход пользователя
    """
    if 'token' not in request.session.keys():
        return Response(data={'message': 'Нет текущего пользователя'}, status=400)

    token = request.session['token']
    user = User.objects.filter(token=token)[0]
    user.token = None
    user.save()
    del request.session['token']
    return Response(data={'message': 'Пользователь вышел'}, status=200)

