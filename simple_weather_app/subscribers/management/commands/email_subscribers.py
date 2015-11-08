from django.core.management.base import BaseCommand, CommandError
from subscribers.utils import send_email_confirmation
from subscribers.models import WeatherSubscriber, get_current_conditions_and_history
import csv
import os

class Command(BaseCommand):
    args = 'send emails out'
    help ='''
    -For each recipient:
        -In all cases the email should be sent to the recipient's entered email address and come from your email address
        - The body of the email can be formatted however you like.  
            - It should contain a readable version of the recipient's location along with the current temperature and weather. 
            - For example, "55 degrees, sunny."
        - fetch the current weather for that recipient's location and change the subject of the email based on the weather (http://www.wunderground.com/weather/api). 
            - If it's nice outside (either sunny or 5 degrees warmer than the average temperature for that location at that time of year), 
                - the email's subject should be "It's nice out! Enjoy a discount on us." 
            - elif's it's not so nice out (either precipitating or 5 degrees cooler than the average temperature at that time of year),
                 - the subject should be "Not so nice out? That's okay, enjoy a discount on us." 
            - else
                - the email subject should read simply "Enjoy a discount on us." 

            - extra: tie in foursqaures location api (https://developer.foursquare.com/start/search/https://developer.foursquare.com/docs/venues/explore) by searching for venues nearby them and returing top ten cheapest priced items: https://developer.foursquare.com/docs/venues/menu.html'''

    def handle(self, *args, **options):
        w_subs = WeatherSubscriber.objects.all()
        history_cache = {}
        for x in w_subs:
            email_addr = x.email
            locale = x.generate_city_state_slug()
            if locale in history_cache:
                locale_data = history_cache[locale]
            else:
                locale_data = get_current_conditions_and_history(x.latitude, x.longitude)
                history_cache[locale] = data

            mean_day_temp = (locale_data['history_high_temp'] + locale_data['history_low_temp'])/float(2)
            if (locale_data['current_temp'] >= mean_day_temp) or 'sunny' in locale_data['current_cond'].lower():
                subject = "It's nice out! Enjoy a discount on us."
            elif (locale_data['current_temp'] <= mean_day_temp) or locale_data['current_precip'] > 0:
                subject = "Not so nice out? That's okay, enjoy a discount on us."
            else:
                subject = "Enjoy a discount on us."

            body = 'Hello!\n\nCurrently for today, %s, it is %s degrees, and %s.\n\n' % (locale, locale_data['current_temp'], locale_data['current_cond'])


            
            