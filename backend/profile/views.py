import uuid
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from rest_framework.response import Response

from .models import Profile

def basicView(request):
    html = "<html><body>Hello!</body></html>"
    return HttpResponse(html)

def registerUser(request):
    if request.method == 'POST':
        User.objects.create(username=request.REQUEST.get('username'),
                            password=request.REQUEST.get('password'))
        user = authenticate(username=request.REQUEST.get('username'),
                            password=request.REQUEST.get('password'))
        login(request, user)
        profile = Profile(user=user, phone=request.REQUEST.get('phone', None))
        image_name = uuid.uuid4()
        photo = request.FILES['image']
        with open(f'../../uploads/photos/{image_name}.img', 'wb+') as p:
            for chunk in photo.chunks():
                p.write(chunk)
        profile.photo = image_name
        profile.save()

def loginUser(request):
    if (request.method == 'POST'):
        user = authenticate(username=request.REQUEST.get('username'),
                            password=request.REQUEST.get('password'))
        login(request, user)

def profile(request):
    if (request.method == 'GET'):
        data = []

        return Response()
    if (request.method == 'POST'):
        pass


# Можно вставлять и настоящие HTML-файлы, посмотрите в Django
