from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from . import views
from . import raw_peers_views

urlpatterns = [
    path('', views.SelfReviewByUserView.as_view(), name='index'),
    url(r'^registration/$', views.registration, name='registration'),
    path('peers/all/', raw_peers_views.get_all_peers),
    path('peers/my/', raw_peers_views.get_all_current_user_peers),
    path('peers/delete/', raw_peers_views.delete_peers),
    path('peers/save/', raw_peers_views.save_peers)
]
