def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]  # Get first IP in the list
    else:
        ip = request.META.get("REMOTE_ADDR")  # Direct IP if no proxy
    return ip
