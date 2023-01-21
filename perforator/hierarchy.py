from .models import Profile, Tokens, Team
from .token import tokenCheck


def __format_profile_to_data(p):
    return {
        'user_id': p.user.id,
        'profile_id': p.id,
        'phone': p.phone,
        'username': p.user.first_name,
        'photo': p.photo.url,
        'sbis': p.sbis,
        'approve': p.approve,
        'message': "ok",
    }


def __format_profile_to_data_without_photo(p):
    # Фото дольше грузится, что для выгрузки полного дерева недопустимо
    return {
        'user_id': p.user.id,
        'profile_id': p.id,
        'username': p.user.first_name,
        'sbis': p.sbis
    }


def get_manager(request):
    """
        Возвращает менеджера текущего пользователя (с фото)
        request.data: не нужна
        :return: Один из следующих словраей:
        Успех: {'user_id': p.user.id, 'profile_id': p.id, 'username': p.user.first_name,
            'photo': base64.b64encode(p.photo.read()), 'sbis': p.sbis },
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]
        team = Team.objects.filter(id=profile.team_id)[0]
        if team.manager:
            return __format_profile_to_data(team.manager)
        else:
            return {'error': True, 'message': 'Менеджер отсутствует'}
    else:
        return {'message': 'Вы не авторизовались'}


def get_manager_status(request):
    """
    Возвращает статус менеджера для указанного profile_id.
    :param request: Принимает JSON { "profile_id": <id> }
    :return: result: Поле "is_manager" либо True либо False
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        profile_id = request.data['profile_id']
        profile = Profile.objects.filter(id=profile_id).first()

        if profile:
            result['is_manager'] = str(profile.is_manager)
            result['status'] = 'ok'
        else:
            result['status'] = 'Профиль не найден'
    else:
        result['status'] = 'You are not login'
    return result


def become_manager(request):
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]

        team = Team.objects.create(manager=profile)
        team.save()

        profile.is_manager = True
        #profile.team_id = team.id
        profile.save()

        result['status'] = 'ok'
    else:
        result['status'] = 'You are not login'
    return result


def update_team(request):
    """
    Добавляет указанного пользователя в команду залогинненого профиля
    :param request: Принимает JSON в формате { "profile_id": <id> }
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        profile_id = request.data['profile_id']
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        manager_profile = Profile.objects.filter(user=user)[0]
        employee_profile = Profile.objects.filter(id=profile_id)[0]
        team = Team.objects.filter(manager=manager_profile).first()

        employee_profile.team_id = team.id
        employee_profile.save()

        result['status'] = 'ok'
    else:
        result['status'] = 'You are not login'
    return result


def delete_user_from_team(request):
    """
    Удаляет указанного пользователя из команды залогинненого профиля
    :param request: Принимает JSON в формате { "profile_id": <id> }
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        profile_id = request.data['profile_id']
        employee_profile = Profile.objects.filter(id=profile_id)[0]

        employee_profile.team_id = None
        employee_profile.save()

        result['status'] = 'ok'
    else:
        result['status'] = 'You are not login'
    return result


# Метод на изменение менеджера (пока не нужен)
# def set_manager(request):
#     if request.user.is_authenticated:
#         profile = Profile.objects.filter(user=request.user)[0]
#         manager_id = request.POST.get('manager_id')
#         if not manager_id:
#             profile.manager_id = None
#         profile.manager_id = request.manager_id
#         return {'message': 'ОК'}
#     else:
#         return {'error': True, 'message': 'Вы не авторизовались'}


def get_team(request):
    """
        Возвращает команду текущего пользователя (с фото)
        request.data: не нужна
        :return: Один из следующих словраей:
        Успех: [{'user_id': p.user.id, 'profile_id': p.id, 'username': p.user.first_name,
            'photo': base64.b64encode(p.photo.read()), 'sbis': p.sbis }, {...}, {...}]
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user).first()
        team = Team.objects.filter(manager=profile).first()

        teams = Profile.objects.filter(team_id=team.id)
        result = []
        for t in teams:
            result.append(__format_profile_to_data(t))
        return result
    else:
        return {'message': 'Вы не авторизовались'}


def get_full_tree():
    """
        Возвращает глобальное дерево иерархии без фото для отладки
        request.data: не нужна
        :return:
        [{'user_id': p.user.id, 'profile_id': p.id, 'username': p.user.first_name,
            'photo': base64.b64encode(p.photo.read()), 'sbis': p.sbis, team:
                [{'user_id': p.user.id, 'profile_id': p.id, 'username': p.user.first_name,
                'photo': base64.b64encode(p.photo.read()), 'sbis': p.sbis, team: [{...}, {...}, {...}],
                {...},
                {...}]
        }]
    """
    current_profile = Profile.objects.first()
    while current_profile.manager:
        current_profile = current_profile.manager

    def recursive_hierarchy_check(profile):
        result = []
        result.append(__format_profile_to_data_without_photo(profile))
        team = profile.team.all()
        if team:
            result[-1]['team'] = []
            for subject in team:
                subject_data = recursive_hierarchy_check(subject)
                result[-1]['team'].append(subject_data)
        return result
    result = recursive_hierarchy_check(current_profile)
    return result


def get_all_users(request):
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        result['users'] = []
        users = Profile._meta.model.objects.all()
        for u in users:
            result['users'].append(__format_profile_to_data(u))
        result['status'] = 'ok'
        print(result['users'])
    else:
        result['status'] = 'You are not login'
    return {'s': "ok"}
