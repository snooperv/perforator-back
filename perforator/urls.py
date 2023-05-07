from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views
from . import raw_peers_views
from . import raw_reviews_views
from . import raw_hierarchy_views
from . import general_views
from . import one_to_one_views
from . import mark_views


urlpatterns = [
    path('', views.SelfReviewByUserView.as_view(), name='index'),
    path('registration/', csrf_exempt(views.registration), name='registration'),
    path('imanager/employee/', views.Employee.as_view(), name='employee'),
    #path('imanager/employee/rating', raw_peers_views.get_user_rating_by_id),

    path('peers/all/', raw_peers_views.get_all_peers),
    path('peers/my/', raw_peers_views.get_all_current_user_peers),
    path('peers/delete/', raw_peers_views.delete_peers),
    path('peers/save/', raw_peers_views.save_peers),
    path('peers/id', raw_peers_views.get_where_user_id_is_peer),
    path('peers/uid', raw_peers_views.get_user_peers),
    path('peers/delete/user', raw_peers_views.delete_user_peers),
    path('peers/save/user', raw_peers_views.save_user_peers),
    path('peers/approve', raw_peers_views.approve_user),

    path('self-review/', raw_reviews_views.get_self_review),
    path('self-review/id', raw_reviews_views.get_self_review_by_id),  #!
    path('self-review/save/', raw_reviews_views.edit_self_review),
    path('self-review/is-draft/', raw_reviews_views.get_is_draft_status),

    path('review/save/', raw_reviews_views.save_review),
    path('review/get/', raw_reviews_views.get_review),

    path('manager', raw_hierarchy_views.get_profile_manager),
    path('manager/become', raw_hierarchy_views.post_become_manager),
    path('manager/status', raw_hierarchy_views.manager_status),
    path('all_users', raw_hierarchy_views.all_users),

    path('api/login', general_views.login_token),
    path('api/refresh-token', general_views.refresh_token),
    path('api/myprofile', general_views.my_profile),
    path('api/companies', general_views.get_companies),
    path('rate_list', general_views.get_irate_list),

    path('1to1/get_common_notes/', one_to_one_views.get_common_notes),
    path('1to1/update_common_notes/', one_to_one_views.update_common_notes),
    path('1to1/get_private_notes/', one_to_one_views.get_private_notes),
    path('1to1/update_private_notes/', one_to_one_views.update_private_notes),

    path('team', raw_hierarchy_views.get_profile_team),
    path('team/update', raw_hierarchy_views.team_update),
    path('team/delete_user', raw_hierarchy_views.team_delete_user),

    path('performance_review/begin', general_views.begin_performance_review),
    path('performance_review/close', general_views.close_performance_review),
    path('performance_review/next_stage', general_views.begin_next_stage),
    path('performance_review/status', general_views.get_pr_status),
    path('performance_review/list', general_views.get_pr_list),
    path('performance_review/get/self_review', raw_reviews_views.pr_get_self_review),
    path('performance_review/get/review', general_views.pr_get_review),
    path('performance_review/get/common_notes', general_views.pr_get_common_notes),
    path('performance_review/get/private_notes', general_views.pr_get_private_notes),
    #path('performance_review/employee/rating', general_views.get_user_rating_by_id),

    path('questionary/create', mark_views.create_questionary),
    path('questionary/update', mark_views.update_questionary),
    path('questionary/get', mark_views.get_questionary),
]
