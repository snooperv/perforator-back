from .models import Profile, Tokens, PerformanceProcess, Team, PrList, Review, Questionary, Question, Answer
from .token import tokenCheck


def questionary_create(request):
    """
    {
        "mark_system": 4,
        "is_self_review": true,
        "questions": [
            {
                "name": "test1",
                "description": "test111"
            },
            {
                "name": "test2",
                "description": "test222"
            }
        ]
    }
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]

        if profile.is_manager:
            perforator = PrList.objects.filter(id=profile.pr).first().pr
            if perforator:
                q = Questionary.objects.filter(profile=profile, perforator=perforator,
                                               is_self_review=data['is_self_review'])
                if q:
                    return {'status': 'Вы уже создали анкету данного типа. Используйте update для изменения.'}
                questionary = Questionary(
                    profile=profile,
                    perforator=perforator,
                    mark_system=data['mark_system'],
                    is_self_review=data['is_self_review']
                )
                questionary.save()

                for q in data['questions']:
                    question = Question(
                        questionary=questionary,
                        name=q['name'],
                        description=q['description']
                    )
                    question.save()
                    result['status'] = 'ok'
            else:
                result['status'] = 'У пользователя отсутствуют активные performance-review'
        else:
            result['status'] = 'Недостаточно прав'
    else:
        result['status'] = 'You are not login'
    return result


def questionary_update(request):
    """
    {
        "mark_system": 4,
        "is_self_review": true,
        "questions": [
            {
                "name": "test1",
                "description": "test111"
            },
            {
                "name": "test2",
                "description": "test222"
            }
        ]
    }
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]

        if profile.is_manager:
            perforator = PrList.objects.filter(id=profile.pr)[0].pr
            if perforator:
                questionary = Questionary.objects.filter(
                    profile=profile,
                    perforator=perforator,
                    is_self_review=data['is_self_review']
                ).first()

                if questionary:
                    questions = Question.objects.filter(questionary=questionary)

                    for i in range(len(questions)):
                        questions[i].name = data['questions'][i]['name']
                        questions[i].description = data['questions'][i]['description']
                        questions[i].save()
                        result['status'] = 'ok'
                else:
                    result['status'] = 'У пользователя отсутствуют анкеты'
            else:
                result['status'] = 'У пользователя отсутствуют активные performance-review'
        else:
            result['status'] = 'Недостаточно прав'
    else:
        result['status'] = 'You are not login'
    return result


def questionary_get(request):
    """
        Возвращает анкету с вопросами залогиненного менеджера.
        Формат входных данных JSON:
        {
            "is_self_review": true
        }
    """
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        token = Tokens.objects.filter(token_f=request.headers['token']).first()
        user = token.user
        profile = Profile.objects.filter(user=user)[0]

        if profile.is_manager:
            perforator = PrList.objects.filter(id=profile.pr)[0].pr
            if perforator:
                questionary = Questionary.objects.filter(
                    profile=profile,
                    perforator=perforator,
                    is_self_review=data['is_self_review']
                ).first()

                if questionary:
                    questions = Question.objects.filter(questionary=questionary)
                    result['questions'] = []
                    for i in range(len(questions)):
                        result['questions'].append({
                            'name': questions[i].name,
                            'description': questions[i].description
                        })
                    result['status'] = 'ok'
                else:
                    result['status'] = 'У пользователя отсутствуют анкеты'
            else:
                result['status'] = 'У пользователя отсутствуют активные performance-review'
        else:
            result['status'] = 'Недостаточно прав'
    else:
        result['status'] = 'You are not login'
    return result
