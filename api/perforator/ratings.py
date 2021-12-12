from .models import PeerReviews, Profile
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


def get_review_from_current_user(request, profile_rated):
    if request.user.is_authenticated:
        cur_profile = Profile.objects.filter(user=request.user)[0]
        return get_review_to_profile(request, cur_profile, profile_rated)
    else:
        return {"error": 'Вы не авторизованы'}


def get_review_to_profile(request, profile_from, profile_rated):
    """
        Возвращает запись в таблицы PeerReviews -
        ревью от пользователя profile_from по отн-ю к
        пользователю profile_rated
        profile_from, profile_rated - запись из модели Profile
        :return: словарь с данными (ключи называются также,
        как и в моделе PeerReviews) или ошибкой
    """
    if request.user.is_authenticated:
        review = PeerReviews.objects.filter(rated_person=profile_rated) \
            .filter(peer_id=profile_from).first()
        answer = {}
        if review is not None:
            answer = dict(review)
            answer['created'] = True
        else:
            answer['created'] = False
        return answer
    else:
        return {"error": 'Вы не авторизованы'}


def generate_review_form_from_current_user(request, profile_rated):
    if request.user.is_authenticated:
        cur_profile = Profile.objects.filter(user=request.user)[0]
        return generate_review_form(request, cur_profile, profile_rated)
    else:
        return {"error": 'Вы не авторизованы'}


def generate_review_form(request, profile_from, profile_rated):
    """
        :return: форму из таблицы PeerReviews, новая пустая форма или
        словарь с ошибкой
    """
    if request.user.is_authenticated:
        review = get_review_to_profile(request, profile_from, profile_rated)

        if review['created'] == False:
            return create_review_form(request)
        del review['created']
        del review['peer_id']
        del review['rated_person']
        return RateForm(initial=review)
    else:
        return {"error": 'Вы не авторизованы'}


def save_review_form_from_current_user(request, profile_rated, form):
    if request.user.is_authenticated:
        cur_profile = Profile.objects.filter(user=request.user)[0]
        return save_review_form(request, cur_profile, profile_rated, form)
    else:
        return {"error": 'Вы не авторизованы'}


def save_review_form(request, profile_from, profile_rated, form):
    """
        :return: словарь с ответом или ошибкой
    """
    if request.user.is_authenticated:
        if form.is_valid():
            review, created = PeerReviews.objects \
                .update_or_create(peer_id=profile_from,
                                  rated_person=profile_rated,
                                  defaults=form.cleaned_data)
            review.save()
            return {'message': 'OK'}
        else:
            return {'error': 'Невалидная форма', 'form': form}
    else:
        return {"error": 'Вы не авторизованы'}


def generate_matched_profiles_and_forms_from_current_user(request):
    if request.user.is_authenticated:
        cur_profile = Profile.objects.filter(user=request.user)[0]
        return generate_matched_profiles_and_forms(request, cur_profile)
    else:
        return {"error": 'Вы не авторизованы'}


def generate_matched_profiles_and_forms(request, profile_from):
    """
        :return: словарь след. вида:
        { profile_object: rate_form, ... }
        или словарь с ошибкой
    """
    if request.user.is_authenticated:
        reviews = PeerReviews.objects.filter(peer_id=profile_from)
        if (len(reviews) == 0):
            return {}

        answer = {}
        for r in reviews:
            form = generate_review_form(request, profile_from, r.rated_person)
            answer[r.rated_person] = form
        return answer
    else:
        return {"error": 'Вы не авторизованы'}
