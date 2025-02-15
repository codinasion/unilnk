from django.contrib.sessions.models import Session
from django.utils.timezone import now


def get_active_users():
    active_sessions = Session.objects.filter(expire_date__gte=now())
    return active_sessions.count()


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # Get first IP in the list
    else:
        ip = request.META.get("REMOTE_ADDR")  # Direct IP if no proxy
    return ip
