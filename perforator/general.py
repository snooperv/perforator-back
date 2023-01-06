import pytz
import hashlib
import random
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Profile, Tokens
from .token import tokenCheck


def login(request):
    utc = pytz.UTC
    result = {'status': 'not ok'}
    user = request.data['user']
    user_data = User.objects.filter(username=user['id']).first()
    if user_data:
        if check_password(user['password'], user_data.password):
            request_time = (datetime.now()).replace(tzinfo=utc)
            get_token_f = get_token_f = hashlib.sha256(("token" + str(random.randint(0, 100000))).encode('utf-8')).hexdigest()
            get_token_b = hashlib.sha256(user['id'].encode('utf-8')).hexdigest()
            token_time_f = (request_time + timedelta(minutes=5)).replace(tzinfo=utc)
            token_time_b = (request_time + timedelta(days=7)).replace(tzinfo=utc)

            tokens = Tokens.objects.filter(user=user_data)

            if len(tokens) == 0:
                new_token = Tokens(user=user_data,
                                   token_f=get_token_f,
                                   token_b=get_token_b,
                                   time_f=token_time_f,
                                   time_b=token_time_b
                                   )
                new_token.save()
                result['token_f'] = get_token_f
                result['token_f_lifetime'] = token_time_f
                result['token_b'] = get_token_b
                result['status'] = 'ok'
                return result
            else:
                token = tokens.first()
                token.time_b = token_time_b
                token.token_b = get_token_b
                token.time_f = token_time_f
                token.token_f = get_token_f
                token.save()

                result['token_f'] = get_token_f
                result['token_f_lifetime'] = token_time_f
                result['token_b'] = get_token_b
                result['status'] = 'ok'
        else:
            result['status'] = 'Неправильный логин или пароль'
    else:
        result['status'] = 'Неправильный логин или пароль'
    return result


def refresh_token(request):
    result = {'status': 'not ok'}
    request_token = request.COOKIES.get('token_b')
    tokens = Tokens.objects.filter(token_b=request_token)

    if len(tokens) == 0:
        result['status'] = 'Отсутствуют сведения об авторизации'
    else:
        utc = pytz.UTC
        token = tokens.first()
        request_time = (datetime.now()).replace(tzinfo=utc)

        if token.time_b < request_time:
            result['status'] = 'Истек период авторизации. Войдите повторно.'
        else:
            token_time_f = (request_time + timedelta(minutes=5)).replace(tzinfo=utc)
            get_token_f = hashlib.sha256(("token" + str(random.randint(0, 100000))).encode('utf-8')).hexdigest()

            token.time_f = token_time_f
            token.token_f = get_token_f
            token.save()

            result['token_f'] = get_token_f
            result['token_f_lifetime'] = token_time_f
            result['status'] = 'ok'
    return result


def my_profile(request):
    """
    USER:  date_joined, email, first_name, groups, id, is_active, is_staff, is_superuser, last_login, las
            t_name, logentry, password, profile, selfreview, user_permissions, username
    :param request:
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]

        result = {
            'name': user.first_name,
            'phone': user.username,
            'sbis': profile.sbis,
            'status': 'ok'
        }
    else:
        result['status'] = 'You are not login'
    return result
