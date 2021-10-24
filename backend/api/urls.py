from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from .views import UserViewSet
from .profile import get_current_user

from .auth_views import auth, login

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^api/v2/current', get_current_user),
    url(r'^api/v2/auth', auth),
    url(r'^api/v2/login', login),
    url(r'^api/v1/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
]
