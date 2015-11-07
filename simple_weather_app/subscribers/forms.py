from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from subscribers.models import WeatherSubscriber, SLUG_CHOICES
from bloom_users.utils import get_geo_coords_data
import time
import sys


class BloomUserQueriesForm(forms.ModelForm):
    city_state_slug = forms.ChoiceField(
        choices=SLUG_CHOICES)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder':'Email'}))
    
    class Meta:
        model = BloomUserQueries
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
        super(BloomUserQueriesForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        for key,value in search_terms_map.iteritems():
            self.fields[key] = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Example: ' +', '.join(value)}))

    def clean(self):
        instance = getattr(self, 'instance', None)
        #print instance
        super(BloomUserQueriesForm, self).clean()
        for key,value in search_terms_map.iteritems():
            if key in self.cleaned_data:
                if len(self.cleaned_data[key].strip()) < 1:
                    raise forms.ValidationError(_('Please include your words/phrases for "%s"' % (key)))
            else:
                raise forms.ValidationError(_('Please include your words/phrases for "%s"' % (key)))       

        return self.cleaned_data

    def save(self, commit=True, *args, **kwargs):
        instance = super(BloomUserQueriesForm, self).save(commit=False, *args, **kwargs)
        temps = str(time.time())
        utctimestamp = temps.split('.')[0]
        gps = get_geo_coords_data(self.cleaned_data.get('ip_address'), self.cleaned_data.get('user_agent'))
        instance.ip_address = self.cleaned_data.get('ip_address')
        instance.user_agent = self.cleaned_data.get('user_agent')
        instance.latitude = gps[0]
        longitude.longitude = gps[1]

        if commit:
            instance.save()
            if not instance.session_id:
                #video hash + guess-id
                temp_session_hash = '%s %s %s' % (instance.pk, instance.user_agent, instance.ip_address)
                instance.session_id = generate_session_hash(temp_session_hash)
                instance.save()

        return instance