from .models import User, Profile, PeerReviews


def login(request):

    return {}


def my_profile(request):
    """
    USER:  date_joined, email, first_name, groups, id, is_active, is_staff, is_superuser, last_login, las
            t_name, logentry, password, profile, selfreview, user_permissions, username
    :param request:
    :return:
    """
    user = request.user
    profile = Profile.objects.filter(user=user)[0]
    user_data = User.objects.filter(id=request.user.id).first()
    result = {
        'name': user_data.first_name,
        'phone': user_data.username,
        'sbis': profile.sbis
    }
    return result
