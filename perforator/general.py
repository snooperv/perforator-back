import os
import pytz
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Profile, Tokens


def tokenCheck(request_token):
    tokens = Tokens.objects.filter(token_f=request_token)
    if len(tokens) == 0:
        return False
    else:
        utc = pytz.UTC
        token = tokens.first()
        token_life_time = (token.time_f + timedelta(seconds=10)).replace(tzinfo=utc)
        datetime_token = (datetime.now()).replace(tzinfo=utc)

        if token_life_time < datetime_token:
            print(token_life_time, datetime_token)
            return False

        return True


def login(request):
    utc = pytz.UTC
    result = {'status': 'not ok'}
    user = request.data['user']
    user_data = User.objects.filter(username=user['id']).first()
    if user_data:
        if check_password(user['password'], user_data.password):
            datetime_token = (datetime.now()).replace(tzinfo=utc)
            get_token = str(os.urandom(5))
            tokens = Tokens.objects.filter(user=user_data)

            if len(tokens) == 0:
                new_token = Tokens(user=user_data, token_f=get_token, token_b='', time_f=datetime_token)
                new_token.save()
                result['token'] = get_token
                result['is_new_token'] = True
            else:
                token = tokens.first()
                token_life_time = (token.time_f + timedelta(seconds=10)).replace(tzinfo=utc)
                if token_life_time < datetime_token:
                    token.time_f = datetime_token
                    token.token_f = get_token
                    token.save()
                    result['is_new_token'] = True
                    result['token'] = get_token
                    result['status'] = 'ok'
                else:
                    result['is_new_token'] = False
                    result['token'] = token.token_f
                    result['status'] = 'ok'
        else:
            result['status'] = 'wrong password'
    else:
        result['status'] = 'wrong login'
    return result


def my_profile(request):
    """
    USER:  date_joined, email, first_name, groups, id, is_active, is_staff, is_superuser, last_login, las
            t_name, logentry, password, profile, selfreview, user_permissions, username
    :param request:
    :return:
    """
    result = {'status': 'exception'}
    if tokenCheck(request.data['token']):
        token = Tokens.objects.filter(token_f=request.data['token']).first()
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
