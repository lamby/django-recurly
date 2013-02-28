import recurly

from django.conf import settings

recurly.API_KEY = settings.RECURLY_API_KEY

if hasattr(settings, 'RECURLY_JS_PRIVATE_KEY'):
    recurly.js.PRIVATE_KEY = settings.RECURLY_JS_PRIVATE_KEY
