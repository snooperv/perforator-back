from rest_framework import routers
from .views import UserViewSet


# Создаем router и регистрируем наш ViewSet
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
# URLs настраиваются автоматически роутером
urlpatterns = router.urls