import pytz
import hashlib
import random
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Profile, Tokens, PeerReviews, OneToOneReviews
from .token import tokenCheck
from .ratings import get_where_user_id_is_peer, get_where_user_id_is_peer_team, generate_review_form


def login(request):
    utc = pytz.UTC
    result = {'status': 'not ok'}
    user = request.data['user']
    user_data = User.objects.filter(username=user['id']).first()
    if user_data:
        if check_password(user['password'], user_data.password):
            request_time = (datetime.now()).replace(tzinfo=utc)
            get_token_f = hashlib.sha256(("token" + str(random.randint(0, 100000))).encode('utf-8')).hexdigest()
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
        token = tokens.first()
        utc = pytz.UTC
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
            'id': profile.id,
            'name': user.first_name,
            'phone': user.username,
            'sbis': profile.sbis,
            'photo': profile.photo.url,
            'status': 'ok'
        }
    else:
        result['status'] = 'You are not login'
    return result


def irate_list(request):
    """
        :return: словарь след. вида:
        { profile.id: rate_form, ... }
        или словарь с ошибкой
    """
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]
        rated = get_where_user_id_is_peer(request, profile.user.id)
        rated_team = get_where_user_id_is_peer_team(request, profile.user.id)
        if (len(rated) == 0 and len(rated_team) == 0):
            return {}
        answer = {'rated': []}

        for r in rated:
            pid = int(r['profile_id'])
            review = PeerReviews.objects.filter(rated_person_id=pid).filter(peer_id=profile).first()
            if review is None:
                p = Profile.objects.filter(id=pid).first()
                answer['rated'].append({
                    'id': p.user.id,
                    'name': p.user.first_name,
                    'phone': p.user.username,
                    'sbis': p.sbis,
                    'photo': p.photo.url
                })
        for r in rated_team:
            pid = int(r['profile_id'])
            review = PeerReviews.objects.filter(rated_person_id=pid).filter(peer_id=profile).first()
            if review is None:
                p = Profile.objects.filter(id=pid).first()
                answer['rated'].append({
                    'id': p.user.id,
                    'name': p.user.first_name,
                    'phone': p.user.username,
                    'sbis': p.sbis,
                    'photo': p.photo.url
                })
        return answer
    else:
        return {"error": 'Вы не авторизованы'}


def processRate(request):
    """
        peer_id - тот, кто оценивают
        rated_person - тот, кого оценивает

        :return: словарь след. вида:
        { profile.id: rate_form, ... }
        или словарь с ошибкой
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        utc = pytz.UTC
        request_time = (datetime.now()).replace(tzinfo=utc)
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        rated_person = Profile.objects.filter(id=data['profile'])[0]
        peer_id = Profile.objects.filter(user=user)[0]
        peer_review = PeerReviews(
            peer_id=peer_id,
            rated_person=rated_person,
            deadlines=data['deadlines'],
            rates_deadlines=data['rates_deadlines'],
            approaches=data['approaches'],
            rates_approaches=data['rates_approaches'],
            teamwork=data['teamwork'],
            rates_teamwork=data['rates_teamwork'],
            practices=data['practices'],
            rates_practices=data['rates_practices'],
            experience=data['experience'],
            rates_experience=data['rates_experience'],
            adaptation=data['adaptation'],
            rates_adaptation=data['rates_adaptation'],
            rates_date=request_time
        )
        peer_review.save()
        result['status'] = 'ok'
    else:
        result['status'] = 'You are not login'
    return result