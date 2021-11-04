from rest_framework.decorators import api_view
from .models import Review, Grade, GradeCategory
from rest_framework.response import Response
from ..api.models import User
from ..performance_review.models import PerformanceReview
from django.conf import settings


def __formatReviewData(review):
    result = {
        'appraising_person': review.appraising_person_id,
        'evaluated_person': review.evaluated_person,
        'is_draft': review.is_draft,
        'grades': []
    }
    grades = Grade.objects.filter(review=review.id)
    for grade in grades:
        result['grades'].append({
            'category_name': grade.grade_category.name,
            'category_description': grade.grade_category.description,
            'grade': grade.grade,
            'comment': grade.comment,
        })
    return result


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
    if (not review):
        performance_review = PerformanceReview.objects.get(id=settings.PERFORMANCE_REVIEW_ID)
        review = Review(appraising_person=user.id,
                        evaluated_person=user.id,
                        performance_review=performance_review,
                        is_draft=True)
        for grade_category in performance_review.self_review_categories:
            Grade.objects.create(
                review=review,
                grade_category=grade_category,
                grade=None,
                comment=''
            )
    return Response(data=__formatReviewData(review), status=200)


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
        review.objects \
            .filter(grade__grade_category__name=grade['category_name']) \
            .update(grade=grade['grade'], comment=grade['comment'])
    if request.data['is_draft'] == False:
        review.is_draft = False
    review.save()
    return Response(status=200)
