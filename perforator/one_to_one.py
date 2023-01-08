from .models import User, Profile, OneToOneReviews
from .token import tokenCheck


def getCommonNotes(request):
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        result['notes'] = {}
        if data['is_manager']:
            manager = Profile.objects.filter(id=data['manager_id']).first()
            for e_id in data['employee_ids']:
                employee = Profile.objects.filter(id=e_id).first()
                review = OneToOneReviews.objects.filter(manager=manager) \
                    .filter(employee=employee).first()
                if review:
                    result['notes'][e_id] = review.common_notes
                else:
                    result['notes'][e_id] = ''
        else:
            manager = Profile.objects.filter(id=data['manager_id']).first()
            employee = Profile.objects.filter(id=data['employee_ids'][0]).first()
            review = OneToOneReviews.objects.filter(manager=manager) \
                .filter(employee=employee).first()
            if review:
                result['notes'][data['employee_ids'][0]] = review.common_notes
            else:
                result['notes'][data['employee_ids'][0]] = ''
        result['status'] = 'ok'
        return result
    else:
        result['status'] = 'You are not login'
    return result


def updateCommonNotes(request):
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data

        manager = Profile.objects.filter(id=data['manager_id']).first()
        employee = Profile.objects.filter(id=data['employee_id']).first()
        review = OneToOneReviews.objects.filter(manager=manager) \
            .filter(employee=employee).first()

        if review:
            review.common_notes = data['note']
            review.save()
            result['status'] = 'ok'
        else:
            new_common_note = OneToOneReviews(
                manager=manager,
                employee=employee,
                common_notes=data['note'],
                manager_notes='',
                employee_notes=''
            )
            new_common_note.save()
            result['status'] = 'ok'
    else:
        result['status'] = 'You are not login'
    return result


def getPrivateNotes(request):
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data
        manager = Profile.objects.filter(id=data['manager_id']).first()
        employee = Profile.objects.filter(id=data['employee_id']).first()
        review = OneToOneReviews.objects.filter(manager=manager) \
            .filter(employee=employee).first()
        if data['is_manager']:
            if review:
                result['notes'] = review.manager_notes
            else:
                result['notes'] = ''
        else:
            if review:
                result['notes'] = review.employee_notes
            else:
                result['notes'] = ''
        result['status'] = 'ok'
        return result
    else:
        result['status'] = 'You are not login'
    return result


def updatePrivateNotes(request):
    result = {'status': 'not ok'}
    if tokenCheck(request.headers['token']):
        data = request.data

        manager = Profile.objects.filter(id=data['manager_id']).first()
        employee = Profile.objects.filter(id=data['employee_id']).first()
        review = OneToOneReviews.objects.filter(manager=manager) \
            .filter(employee=employee).first()

        if review:
            if data['is_manager']:
                review.manager_notes = data['note']
            else:
                review.employee_notes = data['note']
            review.save()
            result['status'] = 'ok'
        else:
            if data['is_manager']:
                new_note = OneToOneReviews(
                    manager=manager,
                    employee=employee,
                    common_notes='',
                    manager_notes=data['note'],
                    employee_notes=''
                )
                new_note.save()
            else:
                OneToOneReviews(
                    manager=manager,
                    employee=employee,
                    common_notes='',
                    manager_notes='',
                    employee_notes=data['note']
                ).save()
            result['status'] = 'ok'
    else:
        result['status'] = 'You are not login'
    return result
