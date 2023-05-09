from .token import tokenCheck
from .models import Profile, User, Review, PrList,\
    Tokens, Question, Questionary, Answer, Team
from .reviews import __format_review_data

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


def save_rating(profile):
    """ Формат входного JSON:
        {

        }
    """
    result = {'status': 'not ok'}
    if profile.is_manager:
        pass
    else:
        pr = Profile.pr
        manager = Team.objects.filter(id=profile.team_id).first().manager

        m_review = Review.objects.filter(appraising_person=manager, evaluated_person=profile,
                                         pr_id=pr, is_self_review=False).first()
        grades = __format_review_data(m_review)['grades']
        avg_mark = 0
        marks = {}
        for g in grades:
            marks[g.name]['m'] = g.mark  #Оценка менеджера
            marks[g.name]['p'] = 0       #Оценка пира
            avg_mark += g.mark
        avg_mark /= len(grades)
        marks['Средняя оценка']['m'] = avg_mark


    return result

