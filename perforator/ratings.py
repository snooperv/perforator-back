from .models import Profile
from .form import RateForm
from .peers import *

"""
    Модуль для работы с ревью на странице 'Я оцениваю'
"""


def create_review_form(request):
    """
        Создать новую пустую форму forms.RateForm
        :return: пустая forms.RateForm
    """
    return RateForm()


def peer_review_to_dict(review):
    return {
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

