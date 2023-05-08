from .token import tokenCheck
from .models import Profile, User, Review, PrList,\
    Tokens, Question, Questionary, Answer, Team

"""
    Модуль для работы с ревью на странице 'Я оцениваю'
"""


def user_rating(request, id):
    """ Формат входного JSON:
        {
            "id": 1,
            "pr_id": 1
        }
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        profile = Profile.objects.filter(id=id).first()
        result['rating'] = [
            {
                'name': 'Средняя оценка',
                'manager': 0,
                'peer': 0,
                'average': 0
            }
        ]
    else:
        result['status'] = 'You are not login'
    return result

