import uuid
from .models import User, Profile

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
    if request.user.is_authenticated:
        users = User.objects.exclude(username=request.user.username)
        result = []
        for u in users:
            profiles = Profile.objects.filter(user=u)
            if len(profiles) == 0:
                profile = Profile(user=u)
                profile.save()
            profile = Profile.objects.filter(user=u)[0]
            obj = {'user_id': u.id, 'profile_id': profile.id,
                   'username': u.first_name, 'photo': profile.photo.url, 'sbis': profile.sbis}
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
    if request.user.is_authenticated:
        result = []
        user = request.user
        profile = Profile.objects.filter(user=user)[0]
        peers = profile.peers.all()
        for p in peers:
            obj = {'user_id': p.user.id, 'profile_id': p.id,
                   'username': p.user.first_name, 'photo': p.photo.url, 'sbis': p.sbis}
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
    if request.user.is_authenticated:
        profile_ids = request.data
        for p in profile_ids:
            profile_list = Profile.objects.filter(id=p)
            if len(profile_list) == 0:
                return {'error': True, f'message': f'Профиль с таким id не найден: {p}'}
            peer = profile_list[0]
            profile_user = Profile.objects.filter(user=request.user)[0]
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
    if request.user.is_authenticated:
        profile_ids = request.data
        for p in profile_ids:
            profile_list = Profile.objects.filter(id=p)
            if len(profile_list) == 0:
                return {'error': True, f'message': f'Профиль с таким id не найден: {p}'}
            peer = profile_list[0]
            profile_user = Profile.objects.filter(user=request.user)[0]
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
            result.append({'user_id': u.id, 'profile_id': p.id, 'username': u.first_name})

        return result
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


def get_where_current_user_is_peer(request):
    """
        Найти пользователей, у которых залогиненный пользователь
        является пиром
    """
    pass


def get_where_user_id_is_peer(request):
    pass
