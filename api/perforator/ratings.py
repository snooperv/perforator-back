from .models import PeerReviews, Profile
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


def get_user_review(request, profile):
    """
        Возвращает запись в таблицы PeerReviews -
        ревью залогиненного пользовтаеля по отн-ю к
        пользователю profile
        profile - запись из модели Profile
        :return: словарь с данными (ключи называются также,
        как и в моделе PeerReviews) или ошибкой
    """
    if request.user.is_authenticated:
        cur_profile = Profile.objects.filter(user=request.user)[0]
        review = PeerReviews.objects.filter(rated_person=profile) \
            .filter(peer_id=cur_profile).first()
        answer = {}
        if review is not None:
            answer = dict(review)
            answer['created'] = True
        else:
            answer['created'] = False
        return answer
    else:
        return {"error": 'Вы не авторизованы'}


def gen_user_review_form(request, profile):
    """
        Возврашает RateForm, созданную залогинненым пользователем
        по отношению к пользователю profile
        profile - запись из модели Profile
        :return: форму из таблицы PeerReviews, новая пустая форма или
        словарь с ошибкой
    """
    if request.user.is_authenticated:
        review = get_user_review(request, profile)

        if review['created'] == False:
            return create_review_form(request)
        del review['created']
        del review['peer_id']
        del review['rated_person']
        return RateForm(initial=review)
    else:
        return {"error": 'Вы не авторизованы'}


def save_user_review_form(request, profile, form):
    """
        Сохранить форму form, созданную залогиненным пользователем
        по отношению к пользовтаелю profile в таблицу PeerReviews
        profile - запись из модели Profile
        form - RateForm
        :return: словарь с ответом или ошибкой
    """
    if request.user.is_authenticated:
        if form.is_valid():
            cur_profile = Profile.objects.filter(user=request.user)[0]

            new_review = PeerReviews.objects.create(peer_id=1,
                                                    rated_person=1,
                                                    **form.cleaned_data)


def gen_matched_users_and_forms(request):
    """
        Создать или взять из таблицы PeerReviews форму RateForm для всех
        пользователей, у которых залогиненный пользователь является пиром
        :return: словарь след. вида:
        { profile_object: rate_form, ... }
        или словарь с ошибкой
    """
    pass

