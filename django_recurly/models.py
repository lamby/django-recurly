import recurly

from django.conf import settings

recurly.API_KEY = settings.RECURLY_API_KEY
