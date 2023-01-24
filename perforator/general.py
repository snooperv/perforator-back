import pytz
import hashlib
import random
from datetime import datetime, timedelta, timezone
from django.contrib.auth.hashers import check_password
from .models import User, Profile, Tokens, PeerReviews, PerformanceProcess, Team, PrList, Review, Grade, OneToOneReviews
from .token import tokenCheck
from .ratings import get_where_user_id_is_peer, get_where_user_id_is_peer_team

minutes_delta = 60


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
            token_time_f = (request_time + timedelta(minutes=minutes_delta)).replace(tzinfo=utc)
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
                result['token_f_lifetime'] = datetime.utcnow() + timedelta(minutes=minutes_delta)
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
                result['token_f_lifetime'] = datetime.utcnow() + timedelta(minutes=minutes_delta)
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
            token_time_f = (request_time + timedelta(minutes=minutes_delta)).replace(tzinfo=utc)
            get_token_f = hashlib.sha256(("token" + str(random.randint(0, 100000))).encode('utf-8')).hexdigest()

            token.time_f = token_time_f
            token.token_f = get_token_f
            token.save()

            result['token_f'] = get_token_f
            result['token_f_lifetime'] = datetime.utcnow() + timedelta(minutes=minutes_delta)
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
            'status': 'ok',
            'team_id': profile.team_id
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
        pr_id = PrList.objects.filter(id=profile.pr)[0].pr.id
        rated = get_where_user_id_is_peer(request, profile.user.id)
        rated_team = get_where_user_id_is_peer_team(request, profile.user.id)
        if (len(rated) == 0 and len(rated_team) == 0):
            return {}
        answer = {'rated': []}

        if not profile.is_manager:
            for r in rated:
                pid = int(r['profile_id'])
                review = PeerReviews.objects.filter(rated_person_id=pid, peer_id=profile, pr_id=pr_id).first()
                if review is None:
                    p = Profile.objects.filter(id=pid).first()
                    answer['rated'].append({
                        'id': p.user.id,
                        'name': p.user.first_name,
                        'phone': p.user.username,
                        'sbis': p.sbis,
                        'photo': p.photo.url
                    })
        else:
            for r in rated_team:
                pid = int(r['profile_id'])
                review = PeerReviews.objects.filter(rated_person_id=pid, peer_id=profile, pr_id=pr_id).first()
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
        pr_id = PrList.objects.filter(id=peer_id.pr)[0].pr.id
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
            rates_date=request_time,
            pr_id=pr_id
        )
        peer_review.save()
        result['status'] = 'ok'
    else:
        result['status'] = 'You are not login'
    return result


def begin_perforator(request):
    """
     :param request:
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        time = (datetime.now()).replace(tzinfo=pytz.UTC)
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user).first()
        if profile.is_manager:
            team = Team.objects.filter(manager=profile).first()
            perforator = PerformanceProcess(
                is_active=True,
                status=0,
                deadline=time
            )
            perforator.save()

            pr_record = PrList(
                pr=perforator,
                profile=profile,
                is_active=True,
                date=time
            )
            pr_record.save()
            pr_id = PrList.objects.filter(pr=perforator).first().id

            profile.pr = pr_id
            profile.save()

            teams = Profile.objects.filter(team_id=team.id)
            for u in teams:
                u_pr_record = PrList(
                    pr=perforator,
                    profile=u,
                    is_active=True,
                    date=time
                )
                u_pr_record.save()

                u_pr_id = PrList.objects.filter(profile=u, is_active=True)[0].id
                u.pr = u_pr_id
                u.save()

            result['status'] = 'ok'
        else:
            result['status'] = 'Вы не менеджер'
    else:
        result['status'] = 'You are not login'
    return result


def next_stage(request):
    """
     :param request:
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        deadline = datetime.strptime(data['deadline'], "%Y-%m-%dT%H:%M")
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user).first()
        if profile.is_manager:
            prl = PrList.objects.filter(id=profile.pr).first()
            pr = prl.pr

            pr.status += 1
            pr.deadline = deadline
            pr.save()
            result['status'] = 'ok'
        else:
            result['status'] = 'Вы не менеджер'
    else:
        result['status'] = 'You are not login'
    return result


def pr_status(request):
    """
     :param request:
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user).first()
        prl = PrList.objects.filter(id=profile.pr).first()
        if prl:
            pr = prl.pr
            offset = datetime.fromtimestamp(pr.deadline.timestamp()) - datetime.utcfromtimestamp(pr.deadline.timestamp())

            result['pr_status'] = pr.status
            result['deadline'] =  pr.deadline - offset
            result['status'] = 'ok'
        else:
            result['pr_status'] = "Отсутствуют активные performance review"
            result['deadline'] = "None"
            result['status'] = 'no pr'
    else:
        result['status'] = 'You are not login'
    return result


def close_perforator(request):
    """
     :param request:
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user).first()

        if profile.is_manager:
            team = Team.objects.filter(manager=profile).first()
            pr_record = PrList.objects.filter(id=profile.pr).first()
            perforator = pr_record.pr

            perforator.status = 0
            perforator.is_active = False
            perforator.save()

            pr_record.is_active = False
            pr_record.date = perforator.deadline
            pr_record.save()

            profile.pr = -1
            profile.save()

            teams = Profile.objects.filter(team_id=team.id)
            for u in teams:
                u_pr_record = PrList.objects.filter(id=u.pr).first()
                u_pr_record.is_active = False
                u_pr_record.date = perforator.deadline
                u_pr_record.save()

                u.pr = -1
                for peer in u.peers.all():
                    u.peers.remove(peer)
                u.approve = False
                u.save()
            result['status'] = 'ok'
        else:
            result['status'] = 'Вы не менеджер'
    else:
        result['status'] = 'You are not login'
    return result


def pr_list(request):
    """
     :param request:
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user).first()
        prl = PrList.objects.filter(profile=profile)
        result['rp'] = []
        for pr in prl:
            result['rp'].append({"pr_id": pr.id, "closing_date": pr.date})
        result['status'] = "ok"
    else:
        result['status'] = 'You are not login'
    return result


def pr_self_review(request):
    """
     :param request: { "pr_id": <pr_id> }
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]

        review = Review.objects.filter(
            appraising_person=profile.id,
            evaluated_person=profile.id,
            pr_id=request.data['pr_id']).first()

        result = {
            'id': review.id,
            'is_draft': review.is_draft,
            'grades': []
        }
        grades = Grade.objects.filter(review=review.id)
        for grade in grades:
            result['grades'].append({
                'id': grade.id,
                'grade_category_id': grade.grade_category.id,
                'grade_category_name': grade.grade_category.name,
                'grade_category_description': grade.grade_category.description,
                'grade_category_preview_description': grade.grade_category.preview_description,
                'comment': grade.comment,
            })
        result['status'] = "ok"
    else:
        result['status'] = 'You are not login'
    return result


def pr_review(request):
    """ Доступ к любому из ревью имеет любой из пользователей. Возможно стоит добавить ограничений?
     :param request: { "appraising_person": <profile_id>, "evaluated_person": <profile_id>, "pr_id": <pr_id> }
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        pr_id = PrList.objects.filter(id=request.data['pr_id'])[0].pr.id
        review = PeerReviews.objects.filter(
            peer_id=data['appraising_person'],
            rated_person=data['evaluated_person'],
            pr_id=pr_id).first()
        if not review:
            return {'status': 'Self-review не найдено'}

        result = {
            'status': "ok",
            'peer_id': review.peer_id.id,
            'rated_person': review.rated_person.id,
            'deadlines': review.deadlines,
            'approaches': review.approaches,
            'teamwork': review.teamwork,
            'practices': review.practices,
            'experience': review.experience,
            'adaptation': review.adaptation,
            'rates_deadlines': review.rates_deadlines,
            'rates_approaches': review.rates_approaches,
            'rates_teamwork': review.rates_teamwork,
            'rates_practices': review.rates_practices,
            'rates_experience': review.rates_experience,
            'rates_adaptation': review.rates_adaptation
        }
    else:
        result['status'] = 'You are not login'
    return result


def pr_common_notes(request):
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        manager = Profile.objects.filter(id=data['manager_id']).first()
        employee = Profile.objects.filter(id=data['employee_id']).first()
        pr_id = PrList.objects.filter(id=data['pr_id'])[0].pr.id
        review = OneToOneReviews.objects.filter(manager=manager) \
            .filter(employee=employee, pr_id=pr_id).first()
        if review:
            result['notes'] = review.common_notes
        else:
            result['notes'] = ''
        result['status'] = 'ok'
        return result
    else:
        result['status'] = 'You are not login'
    return result


def pr_private_notes(request):
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        manager = Profile.objects.filter(id=data['manager_id']).first()
        employee = Profile.objects.filter(id=data['employee_id']).first()
        pr_id = PrList.objects.filter(id=data['pr_id'])[0].pr.id
        review = OneToOneReviews.objects.filter(manager=manager) \
            .filter(employee=employee, pr_id=pr_id).first()
        if data['is_manager']:
            if review:
                result['notes'] = review.manager_notes
            else:
                result['notes'] = ''
        else:
            if review:
                result['notes'] = review.employee_notes
            else:
                result['notes'] = ''
        result['status'] = 'ok'
        return result
    else:
        result['status'] = 'You are not login'
    return result


def pr_user_rating_by_id(request):
    """
    :param request: JSON-body { "id": <user-id пользователя, чьи оценки необходимы>, "pr_id": <pr_id>}
    :return:
    """
    if tokenCheck(request.headers['token']):
        result = []
        id = request.data['id']
        pr_id = PrList.objects.filter(id=request.data['pr_id'])[0].pr.id
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = User.objects.filter(id=id).first()
        manager = token.user

        p = Profile.objects.filter(user=user.id)[0]
        rates = PeerReviews.objects.filter(rated_person_id=id, pr_id=pr_id)
        obj = {'user_id': p.user.id,
               'username': p.user.first_name,
               'photo': p.photo.url,
               'rates': []}
        for r in rates:
            rate = {'who': r.peer_id_id,
                    'is_manager': False,
                    'manager_name': '',
                    'manager_photo': '',
                    'r_deadline': r.rates_deadlines,
                    'r_approaches': r.rates_approaches,
                    'r_teamwork': r.rates_teamwork,
                    'r_practices': r.rates_practices,
                    'r_experience': r.rates_experience,
                    'r_adaptation': r.rates_adaptation,
                    'deadline': r.deadlines,
                    'approaches': r.approaches,
                    'teamwork': r.teamwork,
                    'practices': r.practices,
                    'experience': r.experience,
                    'adaptation': r.adaptation,
                    'rate_date': r.rates_date
                    }
            if r.peer_id_id == manager.id:
                rate['is_manager'] = True
                rate['manager_name'] = manager.first_name
                rate['manager_photo'] = manager.profile.photo.url
            obj['rates'].append(rate)
        result.append(obj)
        return result
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}
