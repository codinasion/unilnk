from django.utils.deprecation import MiddlewareMixin


class CustomSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                # Superuser: Keep session indefinitely (or set a long expiry)
                request.session.set_expiry(
                    0
                )  # 0 = Browser session (never auto-expires)
        else:
            # Regular users: Apply session timeout
            request.session.set_expiry(180)  # 180 seconds
