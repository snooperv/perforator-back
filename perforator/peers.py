import uuid
from .token import tokenCheck
from .models import User, Profile, Tokens, Team, PrList

"""
    Модуль для работы с пирами пользователей.
    Все методы принимают request
    При успешном выполнении возвращают питоновский словарь/список
    При неудачном выполнении возвращают словарь типа: {'error': True, 'message': 'Текст ошибки'}
    Если пользователь не авторизован - возращается ошибка {'error': True, 'message': 'Вы не авторизованы'}
    Как понять, что резульатат неуспешный? Проверьте, вернулся ли словарь и есть ли в нем ключ 'error'
    с любым значенем
"""


# получить всех пиров
def get_all_peers(request):
    """
        Получить всех доступных пиров. Пока это все пользователи, кроме залогиненного.
        ВАЖНО! Если профиль вдруг не был создан ранее у какого-то пользователя,
        он создастся здесь автоматически
        request.data: не требуется
        :return: Список пользователей в виде:
        [ {'user_id': user.id,
           'profile_id': profile.id,
           'username': user.username,
           'photo': profile.photo.url,
           'sbis': user.sbis},
          { ... }
        ]
    """
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        users = User.objects.exclude(username=user.username)
        result = []
        for u in users:
            profiles = Profile.objects.filter(user=u)
            if len(profiles) == 0:
                profile = Profile(user=u)
                profile.save()
            profile = Profile.objects.filter(user=u)[0]
            obj = {'user_id': u.id, 'profile_id': profile.id,
                   'username': u.first_name, 'photo': profile.photo.url, 'sbis': profile.sbis, 'approve': profile.approve}
            result.append(obj)
        return result
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def get_all_current_user_peers(request):
    """
        Получить текущий список пиров для текущего пользователя
        request.data: не требуется
        :return: Список пользователей в виде:
        [ {'user_id': user.id,
           'profile_id': profile.id,
           'username': user.username,
           'photo': user.photo.url,
           'sbis': user.sbis},
          { ... }
        ]
    """
    if tokenCheck(request.headers['token']):
        result = []
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]
        peers = profile.peers.all()
        for p in peers:
            obj = {'user_id': p.user.id,
                   'profile_id': p.id,
                   'username': p.user.first_name,
                   'sbis': p.sbis,
                   'approve': p.approve,
                   'photo': p.photo.url}
            result.append(obj)
        return result
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def delete_peers(request):
    """
        Удалить список пользователей в качестве пиров текущего пользовтаеля.
        request.data: [ profile_id1, profile_id2, ... ] - список id профиля, которые надо удалить
        :return: Один из следующих словраей:
        { message: "ОК" },
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    if tokenCheck(request.headers['token']):
        profile_ids = request.data
        for p in profile_ids:
            profile_list = Profile.objects.filter(id=p)
            if len(profile_list) == 0:
                return {'error': True, f'message': f'Профиль с таким id не найден: {p}'}
            peer = profile_list[0]
            token = Tokens.objects.filter(
                token_f=request.headers['token']).first()
            user = token.user
            profile_user = Profile.objects.filter(user=user)[0]
            if peer in profile_user.peers.all():
                profile_user.peers.remove(peer)
                profile_user.save()
        return {'message': 'ОК'}
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def save_peers(request):
    """
        Сохранить новый список пользователей в качестве пиров текущего пользовтаеля.
        request.data: [ profile_id1, profile_id2, ... ] - список id профиля, которые надо добавить
        :return: Один из следующих словраей:
        { message: "ОК" }
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    if tokenCheck(request.headers['token']):
        profile_ids = request.data
        for p in profile_ids:
            profile_list = Profile.objects.filter(id=p)
            if len(profile_list) == 0:
                return {'error': True, f'message': f'Профиль с таким id не найден: {p}'}
            peer = profile_list[0]
            token = Tokens.objects.filter(
                token_f=request.headers['token']).first()
            user = token.user
            profile_user = Profile.objects.filter(user=user)[0]
            if peer in profile_user.peers.all():
                continue
            profile_user.peers.add(peer)
            profile_user.save()
        return {'message': 'ОК'}
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def search_peers(request):
    """
        Найти всех пользователей, имя (first_name) которых имеет заданную строку
        request.data: string_to_search - та самая заданная строка
        :return: Список вида:
        [ { 'user_id': user.id,
              'profile_id': profile.id,
              'username': user.username },
          { ... }
        ]
    """
    if request.user.is_authenticated:
        substring = str(request.data)

        users = User.objects.get(first_name__icontains=substring)
        result = []

        for u in users:
            p = Profile.objects.get(user=u)
            result.append({'user_id': u.id, 'profile_id': p.id,
                          'username': u.first_name})

        return result
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def get_where_current_user_is_peer(request):
    """
        Найти пользователей, у которых залогиненный пользователь
        является пиром
    """
    pass


def get_where_user_id_is_peer(request, id):
    """
               Получить текущий список пиров любого пользователя по его id
               request.data: не требуется
               :return: Список пользователей в виде:
               [ {'user_id': user.id,
                  'profile_id': profile.id,
                  'username': user.username,
                  'photo': user.photo.url,
                  'sbis': user.sbis},
                 { ... }
               ]
           """
    if tokenCheck(request.headers['token']):
        result = []
        user = User.objects.filter(id=id).first()
        profiles = Profile.objects.filter(peers__user_id=user.id)
        profile = Profile.objects.filter(user=user).first()
        if not profile.is_manager:
            team = Team.objects.filter(id=profile.team_id)[0]
            manager = team.manager
            obj = {'user_id': manager.user.id, 'profile_id': manager.id,
                   'username': manager.user.first_name, 'photo': manager.photo.url, 'approve': manager.approve}
            result.append(obj)
        for p in profiles:
            obj = {'user_id': p.user.id, 'profile_id': p.id,
                   'username': p.user.first_name, 'photo': p.photo.url, 'approve': p.approve}
            result.append(obj)
        return result
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def get_where_user_id_is_peer_team(request, id):
    """
               Получить текущий список пиров любого пользователя по его id
               request.data: не требуется
               :return: Список пользователей в виде:
               [ {'user_id': user.id,
                  'profile_id': profile.id,
                  'username': user.username,
                  'photo': user.photo.url,
                  'sbis': user.sbis},
                 { ... }
               ]
           """
    if tokenCheck(request.headers['token']):
        result = []
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]
        if profile.is_manager:
            team = Team.objects.filter(manager=profile).first()
            team_id = team.id
        else:
            team_id = profile.team_id
        profiles = Profile.objects.filter(team_id=team_id)
        for p in profiles:
            obj = {'user_id': p.user.id, 'profile_id': p.id,
                   'username': p.user.first_name, 'photo': p.photo.url, 'approve': p.approve}
            result.append(obj)
        return result
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def get_user_peers(request, id):
    if tokenCheck(request.headers['token']):
        result = []
        user = User.objects.filter(id=id).first()
        profile = Profile.objects.filter(user=user)[0]
        peers = profile.peers.all()
        for p in peers:
            obj = {'user_id': p.user.id, 'profile_id': p.id,
                   'username': p.user.first_name, 'photo': p.photo.url, 'sbis': p.sbis, 'approve': p.approve}
            result.append(obj)
        return result
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def delete_user_peers(request, id):
    """
        Удалить список пользователей в качестве пиров текущего пользовтаеля.
        request.data: [ profile_id1, profile_id2, ... ] - список id профиля, которые надо удалить
        :return: Один из следующих словраей:
        { message: "ОК" },
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    if tokenCheck(request.headers['token']):
        profile_ids = request.data
        user = User.objects.filter(id=id).first()
        profile_user = Profile.objects.filter(user=user)[0]
        for p in profile_ids:
            profile_list = Profile.objects.filter(id=p)
            if len(profile_list) == 0:
                return {'error': True, f'message': f'Профиль с таким id не найден: {p}'}
            peer = profile_list[0]
            if peer in profile_user.peers.all():
                profile_user.peers.remove(peer)
                profile_user.save()
        return {'message': 'ОК'}
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def save_user_peers(request, id):
    """
        Сохранить новый список пользователей в качестве пиров текущего пользовтаеля.
        request.data: [ profile_id1, profile_id2, ... ] - список id профиля, которые надо добавить
        :return: Один из следующих словраей:
        { message: "ОК" }
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    if tokenCheck(request.headers['token']):
        profile_ids = request.data
        user = User.objects.filter(id=id).first()
        profile_user = Profile.objects.filter(user=user)[0]
        for p in profile_ids:
            profile_list = Profile.objects.filter(id=p)
            if len(profile_list) == 0:
                return {'error': True, f'message': f'Профиль с таким id не найден: {p}'}
            peer = profile_list[0]

            if peer in profile_user.peers.all():
                continue
            profile_user.peers.add(peer)
            profile_user.save()
        return {'message': 'ОК'}
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def approve_user(request, id):
    """
        Проверяет, является ли пользователь утверждённым или нет (по id указанного пользователя)
    """
    result = {'status': "not ok"}
    if tokenCheck(request.headers['token']):
        user = User.objects.filter(id=id).first()
        profile = Profile.objects.filter(user=user).first()
        if profile:
            profile.approve = True
            profile.save()
            result['status'] = 'ok'
        else:
            result['status'] = 'Профиль не найден'
    else:
        result['status'] = 'You are not login'
    return result

