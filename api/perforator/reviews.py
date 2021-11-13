from .models import Profile, Review, GradeCategory, Grade, PerformanceReview
from django.conf import settings

"""
    Модуль для работы с ревью и селф-ревью.
    Аналогичен модулю peers.py
"""


def __format_review_data(review):
    result = {
        'id': review.id,
        'appraising_person': review.appraising_person_id,
        'evaluated_person': review.evaluated_person,
        'is_draft': review.is_draft,
        'grades': []
    }
    grades = Grade.objects.filter(review=review.id)
    for grade in grades:
        result['grades'].append({
            'id': grade.id,
            'grade_category_id': grade.grade_category.id,
            'grade_category_name': grade.grade_category.name,
            'grade_category_description': grade.grade_category.description,
            'grade': grade.grade,
            'comment': grade.comment,
        })
    return result


def get_self_review(request):
    """
        Возвращает селф-ревью
        Аналогичен возвращению обыкновенного ревью, вынесем функционал в другое место
    """
    if not request.user.is_authenticated:
        return {'error': True, 'message': 'Вы не авторизовались'}
    profile = Profile.objects.filter(user=request.user)[0]
    review = Review.objects.get(
        appraising_person=profile.id,
        evaluated_person=profile.id)
    if (not review):
        performance_review = PerformanceReview.objects.get(id=settings.PERFORMANCE_REVIEW_ID)
        review = Review(appraising_person=profile.id,
                        evaluated_person=profile.id,
                        performance_review=performance_review,
                        is_draft=True)
        for grade_category in performance_review.self_review_categories:
            Grade.objects.create(
                review=review,
                grade_category=grade_category,
                grade=None,
                comment=''
            )
    return __format_review_data(review)


def edit_self_review(request):
    """
        Изменяет селф-ревью
        Аналогичен изменению обыкновенного ревью, вынесем функционал в другое место
    """
    if not request.user.is_authenticated:
        return {'error': True, 'message': 'Вы не авторизовались'}
    profile = Profile.objects.filter(user=request.user)[0]
    review = Review.objects.get(
        appraising_person=profile.id,
        evaluated_person=profile.id)
    for grade in request.data['grades']:
        review.objects \
            .filter(grade__grade_category__id=grade['grade_category_id']) \
            .update(grade=grade['grade'], comment=grade['comment'])
    if not request.data['is_draft']:
        review.is_draft = False
    review.save()
    return {'message': 'ОК'}


def get_empty_review_form(request):
    """
        Возвращает запрошенный набор тем для построения формы ревью
        Требуется роль оцениваемых (менеджер \ пиры \ команда)
        Так как у обыкновенных ревью черновиков нет, возвращать готовые ревью не придётся
        Список не оценённых менеджеров \ пиров \ подчинённых запрашивается отедльно
    """
    categories = []
    if request.GET.get('evaluated_person') in ['manager', 'peers', 'team']:
        categories = getattr(PerformanceReview.objects.get(id=settings.PERFORMANCE_REVIEW_ID),
                             request.GET.get('evaluated_person') + '_review_categories')
    return categories.values('id', 'name', 'description')


def save_review(request):
    """
        Сохраняет ревью на выбранного пользователя
        Сохранять можно только в чистовик, то есть возвращать его больше не придётся
    """
    if not request.user.is_authenticated:
        return {'error': True, 'message': 'Вы не авторизовались'}
    profile = Profile.objects.filter(user=request.user)[0]
    review = Review(appraising_person=profile.id,
                    evaluated_person_id=int(request.data['evaluated_person_id']),
                    performance_review_id=settings.PERFORMANCE_REVIEW_ID,
                    is_draft=False)
    if not request.data['not_enough_data']:
        for grade in request.data['grades']:
            Grade.objects.create(review=review,
                                 grade_category_id=grade['grade_category_id'],
                                 grade=grade['grade'],
                                 comment=grade['comment']
                                 )
    else:
        review.is_not_enough_data = True
    review.save()
    return {'message': 'ОК'}
