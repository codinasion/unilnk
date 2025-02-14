import requests
from ipaddress import ip_address, ip_network
import hmac
from hashlib import sha1
from django.conf import settings
from django.utils.encoding import force_bytes


def ValidateGithubAuth(request):
    """
    Validate Github signature
    """

    try:
        """
        Source: https://simpleisbetterthancomplex.com/tutorial/2016/10/31/how-to-handle-github-webhooks-using-django.html
        """

        # Verify if request came from GitHub
        forwarded_for = "{}".format(request.META.get("HTTP_X_FORWARDED_FOR"))
        client_ip_address = ip_address(forwarded_for)
        whitelist = requests.get("https://api.github.com/meta").json()["hooks"]

        for valid_ip in whitelist:
            if client_ip_address in ip_network(valid_ip):
                break
        else:
            return False

        # Verify the request signature
        header_signature = request.META.get("HTTP_X_HUB_SIGNATURE")
        if header_signature is None:
            return False

        sha_name, signature = header_signature.split("=")
        if sha_name != "sha1":
            return False

        mac = hmac.new(
            force_bytes(settings.GITHUB_WEBHOOK_SECRET),
            msg=force_bytes(request.body),
            digestmod=sha1,
        )
        if not hmac.compare_digest(
            force_bytes(mac.hexdigest()), force_bytes(signature)
        ):
            return False

        # If request reached this point we are in a good shape
        return True
    except:
        return False
