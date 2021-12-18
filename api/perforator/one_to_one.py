from .models import PeerReviews, Profile, OneToOneReviews
from .form import OneToOneForm
from .peers import *
from .hierarchy import *

"""
    Модуль для работы с ревью на странице '1-on-1'
"""


def create_review_form(request):
    """
        Создать новую пустую форму forms.RateForm
        :return: пустая forms.RateForm
    """
    return OneToOneForm()


def one_to_one_review_to_dict(review):
    return {
        'manager': review.manager,
        'employee': review.employee,
        'common_notes': review.common_notes,
        'manager_notes': review.manager_notes,
        'employee_notes': review.employee_notes
    }


def get_review_as_manager(request):
    if request.user.is_authenticated:
        cur_profile = Profile.objects.filter(user=request.user)[0]

        team = get_team(request)
        answer = []
        if len(team) == 0:
            return answer

        for mate in team:
            p = Profile.objects.filter(id=mate['profile_id']).first()
            rev = get_review_to_profile(request, cur_profile, p)
            #del rev['created']
            answer.append(rev)
        return answer
    else:
        return {"error": 'Вы не авторизованы'}


def get_review_from_manager(request):
    if request.user.is_authenticated:
        cur_profile = Profile.objects.filter(user=request.user)[0]

        manager = get_manager(request)
        if 'error' in manager:
            return {}

        manager_profile = Profile.objects.filter(id=manager['profile_id']).first()
        rev = get_review_to_profile(request, manager_profile, cur_profile)
        #del rev['created']
        return rev
    else:
        return {"error": 'Вы не авторизованы'}


def get_review_to_profile(request, manager: Profile, employee):
    if request.user.is_authenticated:
        review = OneToOneReviews.objects.filter(manager=manager) \
            .filter(employee=employee).first()

        answer = {}
        if review is not None:
            answer = one_to_one_review_to_dict(review)
            answer['created'] = True
        else:
            answer['created'] = False
            answer['manager'] = manager
            answer['employee'] = employee
        return answer
    else:
        return {"error": 'Вы не авторизованы'}


def generate_form(request, manager, employee):
    if request.user.is_authenticated:
        review = get_review_to_profile(request, manager, employee)
        return generate_form_from_review(request, review)
    else:
        return {"error": 'Вы не авторизованы'}


def generate_form_from_review(request, review):
    if request.user.is_authenticated:
        if review['created'] == False:
            return create_review_form(request)

        profile = Profile.objects.filter(user=request.user).first()
        if profile.id == review['manager'].id:
            text = review['manager_notes']
        else:
            text = review['employee_notes']
        return OneToOneForm(initial={'common': review['common_notes'], 'personal': text})
    else:
        return {"error": 'Вы не авторизованы'}


def save_json(request, json):
    if request.user.is_authenticated:
        common = json['common']
        personal = json['personal']

        interviews_id = int(json['interviewed'])
        is_manager = bool(json['is_manager'])

        if is_manager:
            key = 'employee_notes'
            manager = Profile.objects.filter(id=interviews_id).first()
            employee = Profile.objects.filter(user=request.user).first()
        else:
            key = 'manager_notes'
            manager = Profile.objects.filter(user=request.user).first()
            employee = Profile.objects.filter(id=interviews_id).first()

        review, created = OneToOneReviews.objects \
            .update_or_create(manager=manager,
                              employee=employee,
                              defaults={key: personal, 'common_notes': common})

        return {'message': 'OK'}
    else:
        return {"error": 'Вы не авторизованы'}


def save_form(request, form):
    if request.user.is_authenticated:
        if form.is_valid():
            d = request.POST.dict()

            common = form.cleaned_data['common']
            personal = form.cleaned_data['personal']

            interviews_id = int(d['interviewed'])
            is_manager = bool(d['is_manager'])

            if is_manager:
                key = 'employee_notes'
                manager = Profile.objects.filter(id=interviews_id).first()
                employee = Profile.objects.filter(user=request.user).first()
            else:
                key = 'manager_notes'
                manager = Profile.objects.filter(user=request.user).first()
                employee = Profile.objects.filter(id=interviews_id).first()

            review, created = OneToOneReviews.objects\
                .update_or_create(manager=manager,
                                  employee=employee,
                                  defaults={key: personal, 'common_notes': common})

            return {'message': 'OK'}
        else:
            return {'error': 'Невалидная форма', 'form': form}
    else:
        return {"error": 'Вы не авторизованы'}


def generate_matched_forms_of_current(request):
    if request.user.is_authenticated:
        cur_profile = Profile.objects.filter(user=request.user)[0]
        return generate_matched_forms(request, cur_profile)
    else:
        return {"error": 'Вы не авторизованы'}


def generate_matched_forms(request):
    """
        :return: [ [profile_to, form, is_manager], [] ]
    """
    if request.user.is_authenticated:
        manager_review = get_review_from_manager(request)
        reviews = get_review_as_manager(request)

        answer = []

        if manager_review:
            manager_form = generate_form_from_review(request, manager_review)
            answer.append([manager_review['manager'], manager_form, True])

        if reviews:
            for r in reviews:
                form = generate_form_from_review(request, r)
                answer.append([r['employee'], form, False])

        return answer
    else:
        return {"error": 'Вы не авторизованы'}

