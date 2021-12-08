from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from . import views
from . import raw_peers_views
from . import raw_reviews_views

urlpatterns = [
    path('', views.SelfReviewByUserView.as_view(), name='index'),
    path('irate/', views.I_Rate.as_view(), name='irate'),
    path('1to1/', views.OneToOne.as_view(), name='1to1'),
    path('imanager/', views.I_Manager.as_view(), name='imanager'),
    url(r'^registration/$', views.registration, name='registration'),

    path('peers/demo', raw_peers_views.peers_demo),
    path('peers/all/', raw_peers_views.get_all_peers),
    path('peers/my/', raw_peers_views.get_all_current_user_peers),
    path('peers/delete/', raw_peers_views.delete_peers),
    path('peers/save/', raw_peers_views.save_peers),

    path('self-review/', raw_reviews_views.get_self_review),
    path('self-review/main', raw_reviews_views.self_review),
    path('self-review/save/', raw_reviews_views.edit_self_review),
    path('review/form/', raw_reviews_views.get_empty_review_form),
    path('review/save/', raw_reviews_views.save_review),
]
