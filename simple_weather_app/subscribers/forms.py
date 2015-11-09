from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from localflavor.us.us_states import STATE_CHOICES
from subscribers.models import WeatherSubscriber, SLUG_CHOICES, TOP_100_CITY_DATA
from subscribers.utils import get_geo_coords_data, email_is_valid_format
import time
import sys


class WeatherSubscriberForm(forms.ModelForm):
    city_state_slug = forms.ChoiceField(
        choices=SLUG_CHOICES)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder':'Email'}))
    
    class Meta:
        model = WeatherSubscriber
        exclude = (
            'city',
            'state',
            'ip_address',
            'user_agent',
            'canvas_tagging',
            'latitude',
            'longitude',
            'created_at',
            'modified_at',
        )

    def __init__(self, *args, **kwargs):
        super(WeatherSubscriberForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

    def clean(self):
        instance = getattr(self, 'instance', None)
        super(WeatherSubscriberForm, self).clean()
        if not email_is_valid_format(self.cleaned_data.get('email')):
            raise forms.ValidationError(_('Please use an valid email address'))

        try:
            ws = WeatherSubscriber.objects.get(email=self.cleaned_data.get('email'))
        except WeatherSubscriber.DoesNotExist:
            ws = None
        
        if ws is not None:
            raise forms.ValidationError(_('This email is already in use. Sorry'))

            
        return self.cleaned_data

    def save(self, commit=True, *args, **kwargs):
        instance = super(WeatherSubscriberForm, self).save(commit=False)
        slug_value = int(self.cleaned_data.get('city_state_slug'))
        t_city  = TOP_100_CITY_DATA[slug_value]['place']
        t_state_short = TOP_100_CITY_DATA[slug_value]['state-short']
        gps = get_geo_coords_data(kwargs['ip_address'], kwargs['user_agent'])
        instance.city = t_city.strip()
        instance.state = dict(STATE_CHOICES)[t_state_short.strip()]
        instance.ip_address = kwargs['ip_address']
        instance.user_agent = kwargs['user_agent']
        instance.latitude = gps[0]
        instance.longitude = gps[1]

        if commit:
            instance.save()

        return instance