from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from localflavor.us.us_states import STATE_CHOICES
from subscribers.models import WeatherSubscriber, SLUG_CHOICES
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
            
        return self.cleaned_data

    def save(self, commit=True, *args, **kwargs):
        instance = super(WeatherSubscriberForm, self).save(commit=False, *args, **kwargs)
        t_city, t_state_short = self.cleaned_data.get('city_state_slug').split(',')
        print t_city, t_state_short
        gps = get_geo_coords_data(self.cleaned_data.get('ip_address'), self.cleaned_data.get('user_agent'))
        instance.city = t_city.strip()
        instance.state = dict(STATE_CHOICES)[t_state_short.strip()]
        instance.ip_address = self.cleaned_data.get('ip_address')
        instance.user_agent = self.cleaned_data.get('user_agent')
        instance.latitude = gps[0]
        longitude.longitude = gps[1]

        if commit:
            instance.save()

        return instance