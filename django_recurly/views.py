from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .client import get_client
from .decorators import recurly_basic_authentication

from . import signals

@csrf_exempt
@recurly_basic_authentication
@require_POST
def push_notifications(request):
    client = get_client()

    name = client.parse_notification(request.raw_post_data)

    try:
        signal = getattr(signals, name)
    except AttributeError:
        return HttpResponseBadRequest("Invalid notification name.")

    signal.send(sender=client, data=client.response)

    return HttpResponse()
