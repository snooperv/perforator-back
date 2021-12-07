from .models import User, Profile
import base64


def __format_profile_to_data(p):
    return {
        'user_id': p.user.id,
        'profile_id': p.id,
        'username': p.user.first_name,
        'photo': base64.b64encode(p.photo.read()),
        'sbis': p.sbis
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
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        if profile.manager:
            return __format_profile_to_data(profile.manager)
        else:
            return {'error': True, 'message': 'Менеджер отсутствует'}
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


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
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user)[0]
        team = profile.team.all()
        result = []
        for t in team:
            result.append(__format_profile_to_data(t))
        return result
    else:
        return {'error': True, 'message': 'Вы не авторизовались'}


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
