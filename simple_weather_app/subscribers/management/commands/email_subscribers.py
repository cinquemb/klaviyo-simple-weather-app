from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from subscribers.utils import get_current_conditions_and_history, get_nearby_fs_venues, get_venue_menu_items, get_current_conditions_and_history_api, SendGridEmailer
from subscribers.models import WeatherSubscriber
import csv
import os
import sys

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
        def format_cheapest_items(menu_items, locale, venue_data):
            max_items = min([len(menu_items), 10])
            if max_items == 0:
                return ''

            message_body = '\n\nCheck out these places nearby %s with affordable menu items:\n\n' % (locale)
            for x in range(0,max_items):
                item = menu_items[x]
                place = venue_data[item['venue_id']]
                temp_message_string = '\tPlace %s (%s):\n\n\t\tDish:%s\n\t\tPrice:%s\n\t\tType:%s\n\n' % (place['name'], place['location'], item['dish_name'], item['dish_price'], item['dish_type'])
                message_body += temp_message_string
            return message_body

        w_subs = WeatherSubscriber.objects.all()
        history_cache = {}
        for x in w_subs:
            email_addr = x.email
            locale = x.generate_city_state_slug()
            '''
            if locale in history_cache:
                locale_data = history_cache[locale]['weather']
                venue_data = history_cache[locale]['venue_data']
                sorted_menu_items = history_cache[locale]['venue_data_menu_items']
            else:
            '''
            if settings.DEBUG == True:
                city = locale.split(',')[0].strip()
                state = locale.split(',')[1].strip()
                print city, state, email_addr

                locale_data = get_current_conditions_and_history_api(x.city, x.state)
                venue_data = {}
                sorted_menu_items = []
            else:
                locale_data = get_current_conditions_and_history(x.latitude, x.longitude)

                venue_data = get_nearby_fs_venues(x.latitude, x.longitude)
                all_menu_items = []
                for key, value in venue_data.items():
                    menu_items = get_venue_menu_items(key)
                    sorted_items = sorted(menu_items, key=lambda k:k['dish_price'])
                    all_menu_items+= sorted_items
                
                sorted_menu_items = sorted(all_menu_items, key=lambda k:k['dish_price'])
                history_cache[locale] = {'venue_data': venue_data, 'venue_data_menu_items': sorted_menu_items, 'weather':locale_data}

            mean_day_temp = (locale_data['history_high_temp'] + locale_data['history_low_temp'])/float(2)
            if (locale_data['current_temp'] >= mean_day_temp) or 'sunny' in locale_data['current_cond'].lower():
                subject = "It's nice out! Enjoy a discount on us."
            elif (locale_data['current_temp'] <= mean_day_temp) or locale_data['current_precip'] > 0:
                subject = "Not so nice out? That's okay, enjoy a discount on us."
            else:
                subject = "Enjoy a discount on us."

            message_body = 'Hello!</br>Currently, %s, it is %s degrees, and %s.</br></br>' % (locale, locale_data['current_temp'], locale_data['current_cond']) + format_cheapest_items(sorted_menu_items, locale, venue_data)
            s = SendGridEmailer()

            print 'Sending email to %s' % (email_addr)
            s.send_email("Cinque","cinquemb@simple_weather_app.localhost", subject, message_body, [email_addr], categories='Test', plaintext_body=message_body)


            
            