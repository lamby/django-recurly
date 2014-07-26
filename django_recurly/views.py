import recurly

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .decorators import recurly_basic_authentication

from . import signals

@csrf_exempt
@recurly_basic_authentication
@require_POST
def push_notifications(request):
    try:
        raw_data = request.body # Django 1.6+
    except AttributeError:
        raw_data = request.raw_post_data

    data = recurly.objects_for_push_notification(raw_data)

    try:
        signal = getattr(signals, data['type'])
    except AttributeError:
        return HttpResponseBadRequest("Invalid notification name.")

    signal.send(sender=request, data=data)

    return HttpResponse()
