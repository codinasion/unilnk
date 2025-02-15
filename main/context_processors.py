from .utils import get_active_users

def active_users(request):
    return {
        'active_users_count': get_active_users(),
    }
