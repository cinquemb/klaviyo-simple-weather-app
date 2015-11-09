from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.template.context_processors import csrf
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.template.loader import render_to_string
from django.db.models.query import QuerySet
from subscribers.forms import WeatherSubscriberForm
import json

def home_page(request):
    subscribers_form = WeatherSubscriberForm()
    data = {
        'subscribers_form': subscribers_form,
    }
    data.update(csrf(request))
    return render(request, 'simple_weather_app/home.html', data)

def subscribers_submission(request):
    output_data = {}
    if request.method == 'POST':
        data = request.POST.copy()
        _user_agent = request.META.get('HTTP_USER_AGENT','')
        _ip_addr = request.META.get('REMOTE_ADDR','')
        _referer = request.META.get('HTTP_REFERER','')
        subscribers_form = WeatherSubscriberForm(data=data)
        if subscribers_form.is_valid():
            subscribers_form = subscribers_form.save(user_agent=_user_agent,ip_address=_ip_addr,canvas_tagging='')
            return HttpResponse('You have successfully subscribed to the weather mailing list!', content_type='application/text')
        else:
            subscribers_form.errors.update(subscribers_form.errors)
            output_data['subscribers_form'] = subscribers_form
            output_data['errors'] = True
            output_data.update(csrf(request))

            return render(request, 'simple_weather_app/ajax_modal.html', output_data)
    else:
        return Http404