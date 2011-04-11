import functools

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, \
    HttpResponseForbidden

def recurly_basic_authentication(fn):
    @functools.wraps(fn)
    def wrapper(request, *args, **kwargs):
        authentication = getattr(settings, 'RECURLY_HTTP_AUTHENTICATION', None)

        # If the user has not setup settings.RECURLY_HTTP_AUTHENTICATION then
        # we trust they are doing it at the web server level.
        if authentication is None:
            return fn(request, *args, **kwargs)

        try:
            method, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
        except KeyError:
            response = HttpResponse()
            response.status_code = 401
            response['WWW-Authenticate'] = 'Basic realm="Restricted"'
            return response

        try:
            if method.lower() != 'basic':
                raise ValueError()

            if auth.strip().decode('base64') != authentication:
                return HttpResponseForbidden()
        except Exception:
            return HttpResponseBadRequest()

        return fn(request, *args, **kwargs)
    return wrapper
