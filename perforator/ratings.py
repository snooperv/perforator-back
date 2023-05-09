from .token import tokenCheck
from .models import Profile, UserRating, Review, PrList,\
    Tokens, Question, Questionary, Answer, Team


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


def user_rating(request, id):
    """ Формат входного JSON:
        {
            "id": 1,
            "pr_id": 1
        }
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        profile = Profile.objects.filter(id=id).first()
        result['rating'] = [
            {
                'name': 'Средняя оценка',
                'manager': 0,
                'peer': 0,
                'average': 0
            }
        ]
    else:
        result['status'] = 'You are not login'
    return result


def save_rating(profile):
    """ Формат входного JSON:
        {

        }
    """
    result = {'status': 'not ok'}
    if profile.is_manager:
        pass
    else:
        manager = Team.objects.filter(id=profile.team_id).first().manager

        m_review = Review.objects.filter(appraising_person=manager, evaluated_person=profile,
                                         pr_id=manager.pr, is_self_review=False).first()

        grades = __get_grades(m_review)
        m_avg, marks = 0, {}
        print(grades)

        for g in grades:
            print(g)
            marks[g['id']]['m'] = g['mark']
            marks[g['id']]['name'] = g['name']
            marks[g['id']]['p'] = 0
            marks[g['id']]['a'] = 0
            m_avg += g['mark']
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
                pr=profile.pr,
                name=marks[e]['name'],
                manager_mark=marks[e]['m'],
                peer_mark=marks[e]['p'],
                average_mark=marks[e]['a'],
            )
            ur.save()
    return result


