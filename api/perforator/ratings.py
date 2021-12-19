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
            answer = peer_review_to_dict(review)
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
            td = transform_form(form)

            # try:
            #     obj = PeerReviews.objects.get(peer_id=profile_from, rated_person=profile_rated)
            #     for key, value in td.items():
            #         setattr(obj, key, value)
            #     obj.save()
            # except PeerReviews.DoesNotExist:
            #     new_values = {'peer_id': profile_from, 'rated_person': profile_rated}
            #     new_values.update(td)
            #     obj = PeerReviews(**new_values)
            #     obj.save()

            review, created = PeerReviews.objects.update_or_create(peer_id=profile_from,
                                  rated_person=profile_rated,
                                  defaults=td)

            return {'message': 'OK'}
        else:
            return {'error': 'Невалидная форма', 'form': form}
    else:
        return {"error": 'Вы не авторизованы'}


def transform_form(form):
    answer = form.cleaned_data
    answer['rates_deadlines'] = int(answer['rates_deadlines'])
    answer['rates_approaches'] = int(answer['rates_approaches'])
    answer['rates_teamwork'] = int(answer['rates_teamwork'])
    answer['rates_practices'] = int(answer['rates_practices'])
    answer['rates_experience'] = int(answer['rates_experience'])
    answer['rates_adaptation'] = int(answer['rates_adaptation'])
    return answer


def generate_matched_profiles_and_forms_from_current_user(request):
    if request.user.is_authenticated:
        cur_profile = Profile.objects.filter(user=request.user)[0]
        return generate_matched_profiles_and_forms(request, cur_profile)
    else:
        return {"error": 'Вы не авторизованы'}


def generate_matched_profiles_and_forms(request, profile_from):
    """
        :return: словарь след. вида:
        { profile.id: rate_form, ... }
        или словарь с ошибкой
    """
    if request.user.is_authenticated:
        rated = get_where_user_id_is_peer(request, profile_from.user.id)
        rated_team = get_where_user_id_is_peer_team(request, profile_from.user.id)
        if (len(rated) == 0 and len(rated_team) == 0):
            return {}
        answer = {}
        for r in rated:
            p = Profile.objects.filter(id=r['profile_id']).first()
            form = generate_review_form(request, profile_from, p)
            answer[p] = form
        for r in rated_team:
            p = Profile.objects.filter(id=r['profile_id']).first()
            form = generate_review_form(request, profile_from, p)
            answer[p] = form
        return answer
    else:
        return {"error": 'Вы не авторизованы'}


def peer_review_to_dict(review):
    return {
            'peer_id': review.peer_id,
            'rated_person': review.rated_person,
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

