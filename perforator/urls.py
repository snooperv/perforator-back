from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views
from . import raw_peers_views
from . import raw_reviews_views
from . import raw_hierarchy_views
from . import token_views

urlpatterns = [
    path('', views.SelfReviewByUserView.as_view(), name='index'),
    path('irate/', views.I_Rate.as_view(), name='irate'),
    path('1to1/', views.OneToOne.as_view(), name='1to1'),
    path('imanager/', views.I_Manager.as_view(), name='imanager'),
    path('registration/', csrf_exempt(views.registration), name='registration'),
    path('process_rate/', csrf_exempt(views.process_rate_form), name='process_rate'),
    path('process_one_to_one/', views.process_one_to_one_form),
    path('imanager/employee/', views.Employee.as_view(), name='employee'),
    path('imanager/employee/rating', raw_peers_views.get_user_rating_by_id),

    path('peers/demo', raw_peers_views.peers_demo),
    path('peers/all/', raw_peers_views.get_all_peers),
    path('peers/my/', raw_peers_views.get_all_current_user_peers),
    path('peers/delete/', raw_peers_views.delete_peers),
    path('peers/save/', raw_peers_views.save_peers),
    path('peers/id', raw_peers_views.get_where_user_id_is_peer),
    path('peers/uid', raw_peers_views.get_user_peers),
    path('peers/delete/user', raw_peers_views.delete_user_peers),
    path('peers/save/user', raw_peers_views.save_user_peers),


    path('self-review/', raw_reviews_views.get_self_review),
    path('self-review/id', raw_reviews_views.get_self_review_by_id),
    path('self-review/main', raw_reviews_views.self_review),
    path('self-review/save/', raw_reviews_views.edit_self_review),
    path('review/form/', raw_reviews_views.get_empty_review_form),
    path('review/save/', raw_reviews_views.save_review),
    path('self-review/is-draft/', raw_reviews_views.get_is_draft_status),

    path('manager', raw_hierarchy_views.get_profile_manager),
    path('team', raw_hierarchy_views.get_profile_team),
    path('hierarchy', raw_hierarchy_views.get_full_hierarchy_tree),

    path('peers/approve', raw_peers_views.approve_user),

    path('api/login', token_views.login_token)
]
