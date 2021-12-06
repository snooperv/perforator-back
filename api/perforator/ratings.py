from .models import PeerReviews
from .form import RateForm
import peers

"""
    Модуль для работы с ревью на странице 'Я оцениваю'
"""


def create_review_form(request):
    """
        Создать новую пустую форму forms.RateForm
        :return: пустая forms.RateForm
    """
    return RateForm()


def get_user_review_form(request, profile):
    """
        Возврашает RateForm, созданную залогинненым пользователем
        по отношению к пользователю profile
        profile - запись из модели Profile
        :return: форму из таблицы PeerReviews, новая пустая форма или
        словарь с ошибкой
    """
    pass


def save_user_review_form(request, profile, form):
    """
        Сохранить форму form, созданную залогиненным пользователем
        по отношению к пользовтаелю profile в таблицу PeerReviews
        profile - запись из модели Profile
        form - RateForm
        :return: словарь с ответом или ошибкой
    """
    pass


def gen_matched_users_and_forms(request):
    """
        Создать или взять из таблицы PeerReviews форму RateForm для всех
        пользователей, у которых залогиненный пользователь является пиром
        :return: словарь след. вида:
        { profile_object: rate_form, ... }
        или словарь с ошибкой
    """
    pass

