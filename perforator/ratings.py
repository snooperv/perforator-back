from .token import tokenCheck
from .models import Profile, UserRating, Review, PrList,\
    Question, TeamRating, Answer, Team, Tokens


def __get_grades(review):
    result = []
    questions = Question.objects.filter(questionary=review.questionary)
    for q in questions:
        answer = Answer.objects.filter(profile=review.appraising_person, question=q, review=review).first()
        if answer:
            result.append({
                'id': q.id,
                'name': q.name,
                'mark': answer.mark
            })
    return result


def user_rating(request):
    """ Возвращает таблицу с оценками пользователя.
        Формат входного JSON:
        {
            "id": 1,
            "pr_id": 1
        }
        id - Идентификатор пользователя, рейтинг которого нужен;
        pr_id - Идентификатор конкретного performance review
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        profile = Profile.objects.filter(id=data['id']).first()
        pr = PrList.objects.filter(id=data['pr_id']).first()
        rating = UserRating.objects.filter(profile=profile, pr=pr)
        if rating:
            result['rating'] = []

            for e in rating:
                result['rating'].append({
                    'name': e.name,
                    'manager': e.manager_mark,
                    'peer': e.peer_mark,
                    'average': e.average_mark
                })
            result['status'] = 'ok'
        else:
            result['status'] = 'Отсутствует информация с рейтингом'
    else:
        result['status'] = 'You are not login'
    return result


def save_user_rating(profile):
    """ Сохраняет рейтинг сотрудника в базу
    """
    result = {'status': 'not ok'}
    if profile.is_manager:
        team = Profile.objects.filter(team_id=Team.objects.get(manager=profile).id)
        pr = PrList.objects.get(id=profile.pr)
        count_marks, marks = 0, {}
        for t in team:
            review = Review.objects.filter(appraising_person=t, evaluated_person=profile,
                                           pr_id=t.pr, is_self_review=False).first()
            if review:
                p_grades = __get_grades(review)
                count_marks += 1
                for g in p_grades:
                    if g['name'] in marks:
                        marks[g['name']] = g['mark']
                    else:
                        marks[g['name']] += g['mark']
        for e in marks:
            marks[e] /= count_marks

            rating = UserRating(
                profile=profile,
                pr=pr,
                name=e,
                average_mark=round(marks[e], 2)
            )
            rating.save()
    else:
        manager = Team.objects.filter(id=profile.team_id).first().manager
        pr = PrList.objects.filter(id=profile.pr).first()
        m_review = Review.objects.filter(appraising_person=manager, evaluated_person=profile,
                                         pr_id=manager.pr, is_self_review=False).first()

        grades = __get_grades(m_review)
        m_avg, marks = 0, {}

        for g in grades:
            marks[g['id']] = {}
            marks[g['id']]['m'] = g['mark']
            marks[g['id']]['name'] = g['name']
            marks[g['id']]['p'] = 0
            marks[g['id']]['a'] = 0
            m_avg += g['mark']

        marks['avg'] = {}
        marks['avg']['name'] = "Средняя оценка"
        marks['avg']['m'] = m_avg / len(grades)
        marks['avg']['p'] = 0
        marks['avg']['a'] = 0

        team = Profile.objects.filter(team_id=profile.team_id)
        count_marks = 0

        for t in team:
            review = Review.objects.filter(appraising_person=t, evaluated_person=profile,
                                           pr_id=t.pr, is_self_review=False).first()
            if review:
                p_grades = __get_grades(review)
                count_marks += 1
                for g in p_grades:
                    marks[g['id']]['p'] += g['mark']
                    marks['avg']['p'] += g['mark']

        marks['avg']['p'] /= (len(grades) * count_marks)
        marks['avg']['p'] = round(marks['avg']['p'], 2)

        for e in marks:
            marks[e]['a'] = round(((marks[e]['m'] + marks[e]['p']) / 2), 2)

            ur = UserRating(
                profile=profile,
                pr=pr,
                name=marks[e]['name'],
                manager_mark=marks[e]['m'],
                peer_mark=marks[e]['p'],
                average_mark=marks[e]['a'],
            )
            ur.save()

    return result


def save_manager_rating(manager, team):
    result = {}
    for u in team:
        pr = PrList.objects.filter(id=u.pr).first()
        rating = UserRating.objects.filter(profile=u, pr=pr)

        for e in rating:
            if e.name not in result:
                result[e.name] = e.average_mark
            else:
                result[e.name] += e.average_mark
    for e in result:
        result[e] /= len(team)
        team_rating = TeamRating(
            manager=manager,
            pr=PrList.objects.filter(id=manager.pr).first(),
            name=e,
            average_mark=round(result[e], 2)
        )
        team_rating.save()


def manager_rating(request, pr_id):
    """
        Возвращает таблицу с рейтингом о команде залогиненного менеджера.
        Входные данные: Это GET-запрос, в параметрах надо передать performance review ID с названием поля "id"
        пример: <url>/rating/manager_get?id=1
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        user = Tokens.objects.filter(token_f=request.headers['token']).first().user
        profile = Profile.objects.filter(user=user).first()

        if profile.is_manager:
            result['rating'] = []
            team_rating = TeamRating.objects.filter(manager=profile, pr=pr_id)
            if team_rating:
                for e in team_rating:
                    result['rating'].append({
                        'name': e.name,
                        'mark': e.average_mark
                    })
                result['status'] = 'ok'
            else:
                result['status'] = 'Отсутствует информация с рейтингом'
        else:
            result['status'] = 'Недостаточно прав. Вы не менеджер'
    else:
        result['status'] = 'You are not login'
    return result
