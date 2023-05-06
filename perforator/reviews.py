from .token import tokenCheck
from .models import Profile, User, Review, PrList, PerformanceReview,\
    Tokens, Question, Questionary, Answer, Team


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

    questions = Question.objects.filter(questionary=review.questionary)
    for q in questions:
        answer = Answer.objects.filter(profile=review.appraising_person, question=q, review=review).first()
        result['grades'].append({
            'id': answer.id,
            'name': q.name,
            'description': q.description,
            'text': answer.text,
            'mark': answer.mark
        })
    return result


def get_self_review(request):
    """ GET метод. Ничего не принимает и возвращает self-review залогиненного пользователя в формате:
    {
        "id": 2,
        "is_draft": true,
        "grades": [
            {
                "id": 5,
                "name": "test1",
                "description": "test111",
                "text": ""
            },
            {
                "id": 8,
                "name": "test2",
                "description": "test222",
                "text": ""
            }
        ]
    }
    В случае ошибки один из вариантов:
        {'status': 'Self-review не найдено'},
        {'status': 'Вы не авторизовались'},
        {'status': <error message>}
    """
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]

        review = Review.objects.filter(
            appraising_person=profile,
            evaluated_person=profile,
            is_self_review=True,
            pr_id=profile.pr).first()
        if not review:
            return {'status': 'Self-review не найдено'}
    else:
        return {'status': 'Вы не авторизовались'}
    return __format_review_data(review)


def edit_self_review(request):
    """ Формат входного JSON:
    {
        "is_draft": true,
        "grades": [
            {
                "id": 5,
                "text": "Ю"
            },
            {
                "id": 8,
                "text": "Фак"
            }
        ]
    }
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]
        review = Review.objects.get(
            appraising_person=profile.id,
            evaluated_person=profile.id,
            is_self_review=True,
            pr_id=profile.pr)
        if review:
            for grade in request.data['grades']:
                Answer.objects.filter(id=grade['id']).update(text=grade['text'])
            if not request.data['is_draft']:
                review.is_draft = False
            review.save()
            result['status'] = 'ok'
        else:
            result['status'] = 'Self-review не найдено'
    else:
        result['status'] = 'You are not login'
    return result


def is_draft(request, id):
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        user = User.objects.filter(id=id).first()
        profile = Profile.objects.filter(user=user).first()
        review = Review.objects.filter(
            appraising_person=profile.id,
            evaluated_person=profile.id,
            is_self_review=True,
            pr_id=profile.pr).first()
        if review:
            result['is_draft'] = review.is_draft
        else:
            result['status'] = 'Review не найдено'
    else:
        result['status'] = 'You are not login'
    return result


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
    """ Формат входного JSON:
    {
        "profile": 2,
        "is_draft": true,
        "grades": [
            {
                "id": 5,
                "text": "Ю",
                "mark": 2
            },
            {
                "id": 8,
                "text": "Фак",
                "mark": 1
            }
        ]
    }
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        appraising_person = Profile.objects.filter(user=user).first()
        evaluated_person = Profile.objects.filter(id=data['profile']).first()
        review = Review.objects.filter(appraising_person=appraising_person,
                                       evaluated_person=evaluated_person,
                                       is_self_review=False,
                                       pr_id=appraising_person.pr).first()
        if review:
            for grade in request.data['grades']:
                Answer.objects.filter(id=grade['id']).update(text=grade['text'], mark=grade['mark'])
            if not request.data['is_draft']:
                review.is_draft = False
            review.save()
            result = {'status': 'ok'}
        else:
            result['status'] = 'Review не найдено'
    else:
        result['status'] = 'You are not login'
    return result


def get_self_review_by_id(request, id):
    """
    TESTED
        Возвращает селф-ревью по указанному id профиля.
        request.GET: необходимо id профиля, для которого нудно получить self-review
        :return: Один из следующих словраей:
        {
            'id': review.id,
            'is_draft': review.is_draft,
            'grades':   [
                {
                    'id': <id ответа>,
                    'name': <название вопроса>,
                    'description': <описание вопроса>,
                    'text': <текст ответа>,
                    'mark': <оценка ответа>
                },
                {...},
                {...}
            ]
        }
        При ошибке: { 'status': 'Self-review не найдено'}
    """
    if tokenCheck(request.headers['token']):
        profile = Profile.objects.filter(id=id).first()
        review = Review.objects.filter(
            appraising_person=id,
            evaluated_person=id,
            pr_id=profile.pr,
            is_self_review=True
        ).first()
        if not review:
            return {'status': 'Self-review не найдено'}
    else:
        return {'status': 'Вы не авторизовались'}
    return __format_review_data(review)


def get_review(request):
    """
    {
        "appraising_person": 1,
        "evaluated_person": 2
    }
    """
    if tokenCheck(request.headers['token']):
        data = request.data

        appraising_person = Profile.objects.filter(id=data['appraising_person']).first()
        evaluated_person = Profile.objects.filter(id=data['evaluated_person']).first()

        if appraising_person.pr == -1:
            return {'status': 'Отсутствуют активные performance review'}
        else:
            pr_id = appraising_person.pr
        review = Review.objects.filter(
            appraising_person=appraising_person,
            evaluated_person=evaluated_person,
            is_self_review=False,
            pr_id=pr_id).first()
        if not review:
            return {'status': 'Review не найдено'}
    else:
        return {'status': 'Вы не авторизовались'}
    return __format_review_data(review)


def pr_self_review(request):
    """
     :param request: { "pr_id": <pr_id> }
    :return:
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]

        review = Review.objects.filter(
            appraising_person=profile,
            evaluated_person=profile,
            is_self_review=True,
            pr_id=request.data['pr_id']).first()

        if review:
            result = __format_review_data(review)
        else:
            result['status'] = 'Review не найдено'
    else:
        result['status'] = 'You are not login'
    return result
