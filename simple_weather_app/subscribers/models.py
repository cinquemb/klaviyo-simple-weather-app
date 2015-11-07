from django.conf import settings
from django.db import models
from localflavor.us.models import USStateField
from localflavor.us.us_states import STATE_CHOICES
from django.db.utils import DatabaseError
from django.core.validators import MinValueValidator


STATE_ABBREVIATIONS = dict(STATE_CHOICES)
SLUG_CHOICES = ((x,y) )

class WeatherSubscriber(models.Model):
	city = models.CharField(max_length=255)
    #two letter state abbrevation
    state = USStateField(choices=STATE_CHOICES)
    email = models.EmailField(null=True, blank=True, db_index=True)
	
	# for finger printing to combat spam
	#https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Basic_usage
	#http://stackoverflow.com/questions/15685698/getting-binary-base64-data-from-html5-canvas-readasbinarystring
	canvas_tagging = models.TextField(null=True,blank=True)
	ip_address = models.TextField(null=True,blank=True)
	user_agent = models.TextField(null=True,blank=True)
	latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
	
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	def generate_city_state_slug(self):
		return self.city + ', ' + self.state