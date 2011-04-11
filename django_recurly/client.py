from recurly import Recurly

from django.conf import settings

def get_client():
    return Recurly(
        username=settings.RECURLY_USERNAME,
        password=settings.RECURLY_PASSWORD,
        subdomain=settings.RECURLY_SUBDOMAIN,
    )
