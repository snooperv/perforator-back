from rest_framework.decorators import api_view
from .models import Review, Grade, GradeCategory
from rest_framework.response import Response
from ..api.models import User


@api_view(['GET'])
def getSelfReview(request):
    """
        Возвращает селф-ревью
        Аналогичен возвращению обыкновенного ревью, вынесем функционал в другое место
    """
    user = User.objects.filter(token=request.session['token'])[0]
    review = Review.objects.get(
        appraising_person=user.id,
        evaluated_person=user.id)
    grades = Grade.objects.filter(review=review.id)
    result = {
        'appraising_person': review.appraising_person_id,
        'evaluated_person': review.evaluated_person,
        'is_draft': review.is_draft,
        'grades': []
    }
    for grade in grades:
        result['grades'].append({
            'category_name': grade.grade_category.name,
            'category_description': grade.grade_category.description,
            'grade': grade.grade,
            'comment': grade.comment,
        })
    return Response(data=result, status=200)


@api_view(['POST'])
def editSelfReview(request):
    """
        Изменяет селф-ревью
        Аналогичен изменению обыкновенного ревью, вынесем функционал в другое место
    """
    user = User.objects.filter(token=request.session['token'])[0]
    review = Review.objects.get(
        appraising_person=user.id,
        evaluated_person=user.id)
    for grade in request.data['grades']:
        review.objects\
            .filter(grade__grade_category__name=grade['category_name'])\
            .update(grade=grade['grade'], comment=grade['comment'])
    if request.data['is_draft'] == False:
        review.is_draft=False
    review.save()
    return Response(status=200)
