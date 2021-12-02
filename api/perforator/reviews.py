from .models import Profile, Review, GradeCategory, Grade, PerformanceReview
from django.conf import settings

"""
    Модуль для работы с ревью и селф-ревью.
    Аналогичен модулю peers.py
"""


def __format_review_data(review):
    result = {
        'id': review.id,
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
            'comment': grade.comment,
        })
    return result


def get_self_review(request):
    """
    TESTED
        Возвращает селф-ревью
        request.GET: параметры не нужны
        :return: Один из следующих словраей:
        { 'id': review.id, 'is_draft': review.is_draft,
        'grades':   [
            { 'id': grade.id, 'grade_category_id': grade.grade_category.id,
            'grade_category_name': grade.grade_category.name, 'grade_category_description': grade.grade_category.description,
            'comment': grade.comment (только коммент. У сэлф-ревью оценка всегда NULL),
            } {...}, {...}
        ] },
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    if not request.user.is_authenticated:
        return {'error': True, 'message': 'Вы не авторизовались'}
    profile = Profile.objects.filter(user=request.user).first()
    print(profile)
    review = Review.objects.filter(
        appraising_person=profile.id,
        evaluated_person=profile.id).first()
    if (not review):
        performance_review = PerformanceReview.objects.get(id=1)
        review = Review.objects.create(appraising_person=profile,
                                       evaluated_person=profile,
                                       performance_review=performance_review,
                                       is_draft=True)
        for grade_category in performance_review.self_review_categories.all():
            Grade.objects.create(
                review=review,
                grade_category=grade_category,
                grade=None,
                comment=''
            )
    return __format_review_data(review)


def edit_self_review(request):
    """
    TESTED
        Изменяет селф-ревью
        Аналогичен изменению обыкновенного ревью, вынесем функционал в другое место
        request.data: (Заполненное селф-ревью)
        { 'id': review.id, 'is_draft': review.is_draft,
        'grades':   [
            {
            'grade_category_id': grade.grade_category.id,
            'comment': grade.comment (только коммент. У сэлф-ревью оценка всегда NULL),
            }, {...}, {...}
        ] }
        :return: Один из следующих словраей:
        { message: "ОК" },
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    if not request.user.is_authenticated:
        return {'error': True, 'message': 'Вы не авторизовались'}
    profile = Profile.objects.filter(user=request.user)[0]
    review = Review.objects.get(
        appraising_person=profile.id,
        evaluated_person=profile.id)
    for grade in request.data['grades']:
        Grade.objects.filter(review=review, grade_category_id=grade['grade_category_id']) \
            .update(grade=None, comment=grade['comment'])
    if not request.data['is_draft']:
        review.is_draft = False
    review.save()
    return {'message': 'ОК'}


def get_empty_review_form(request):
    """
    TESTED
        Возвращает запрошенный набор тем для построения формы ревью
        Так как у обыкновенных ревью черновиков нет, возвращать готовые ревью не придётся
        Список не оценённых менеджеров \ пиров \ подчинённых запрашивается отедльно
        request.GET: параметры не нужны
        :return: Один из следующих словраей:
        { categories:
            manager_review_categories: [
                { id, name, description },
                {...}, {...}
            ],
            peers_review_categories: [ {...}, {...}],
            team_review_categories: [ {...}, {...}],
         },
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    performance_review = PerformanceReview.objects.get(id=1)
    categories = {}
    for role in ['manager', 'peers', 'team']:
        categories_name = role + '_review_categories'
        categories[categories_name] = getattr(performance_review, categories_name).values('id', 'name', 'description')
    return categories


def save_review(request):
    """
        Сохраняет ревью на выбранного пользователя
        Сохранять можно только в чистовик, то есть возвращать его больше не придётся
        request.data: (Заполненное ревью. Аналогично селф-ревью, но:
        все оценки имеют числовой эквивалент;
        is_draft автоматически ставится false;
        есть возможность поставить not_enough_data (если пользователь не может оценить человека))
        { 'id': review.id,
        'evaluated_person': review.evaluated_person_id,
        'is_not_enough_data': boolean
        'grades':   [
            { 'id': grade.id, 'grade_category_id': grade.grade_category.id,
            'grade': grade.grade,
            'comment': grade.comment,
            }, {...}, {...}
        ] }
        :return: Один из следующих словраей:
        { message: "ОК" },
        При ошибке: {'error': True, 'message': 'Профиль с таким id не найден'}
    """
    if not request.user.is_authenticated:
        return {'error': True, 'message': 'Вы не авторизовались'}
    profile = Profile.objects.filter(user=request.user)[0]
    review = Review.objects.create(appraising_person=profile,
                                   evaluated_person_id=int(request.data['evaluated_person_id']),
                                   performance_review_id=1,
                                   is_draft=False)
    if not request.data['is_not_enough_data']:
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
