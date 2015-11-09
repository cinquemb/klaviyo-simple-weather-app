from django.conf import settings
from django.forms import EmailField
from django.core.exceptions import ValidationError
import sendgrid
import urllib
import urllib2
import html2text
import requests
import json
import datetime
import time
import email
import smtplib
from bs4 import BeautifulSoup as bs
import re

def get_nearby_fs_venues(lat,lng):
    url = 'https://api.foursquare.com/v2/venues/search?ll=%s,%s&oauth_token=G0DX0Z5SEQZRNQ3KTG24LO1REZMF2A12VVK32ZJUNOL4C4NC&v=20151108' % (lat, lng)#, settings.FOURSQUARE_CLIENT_ID, settings.FOURSQUARE_CLIENT_SECRET)
    r = requests.get(url)
    nb_fs_venues = json.loads(r.text)
    if 'groups' in nb_fs_venues['response']:
        nb_fs_venues_data = {x['venue']['id']: {'name': x['venue']['name'],'location': x['venue']['location']} for x in nb_fs_venues['response']['groups'][0]['items']}
    else:
        nb_fs_venues_data = {}
    return nb_fs_venues_data

def get_venue_menu_items(venue_id):
    url = 'https://api.foursquare.com/v2/venues/%s/menu?oauth_token=G0DX0Z5SEQZRNQ3KTG24LO1REZMF2A12VVK32ZJUNOL4C4NC&v=20151108' % (venue_id)#, settings.FOURSQUARE_CLIENT_ID, settings.FOURSQUARE_CLIENT_SECRET)
    r = requests.get(url)
    menu_items = json.loads(r.text)

    dishes = []
    for menu in menu_items['response']['menu']['menus']['items']:
        for x in menu['entries']['items']:
            for y in x['entries']['items']:
                dish_name = y['name']
                dish_price = float(y['price'])
                dish_type = x['name']
                dishes.append({'dish_name': dish_name, 'dish_price': dish_price, 'dish_type': dish_type, 'venue_id': venue_id})
    return dishes

def format_temp(temp):
    return float(re.sub("[^0-9\.]", "", temp.strip()))


def get_current_conditions_and_history_api(city, state_short):
    format_city = '_'.join(city.title().split(' '))
    url = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (settings.WUNDERGROUND_KEY, state_short, format_city)
    r = requests.get(url)
    curr_day = '_'.join(datetime.date.fromtimestamp(time.time()).isoformat().split('-'))
    url_h = 'http://api.wunderground.com/api/%s/history_%s/q/%s/%s.json' % (settings.WUNDERGROUND_KEY, curr_day, state_short, format_city)
    r_h = requests.get(url_h)
    current_conditions_data = json.loads(r.text)
    historical_conditions_data = json.loads(r_h.text)

    current_temp = float(current_conditions_data['current_observation']['temp_f'])
    current_precip = float(current_conditions_data['current_observation']['precip_today_in'])
    current_cond = current_conditions_data['current_observation']['weather']

    history_high_temp = float(historical_conditions_data['history']['dailysummary'][0]['meantempm'])
    history_low_temp = float(historical_conditions_data['history']['dailysummary'][0]['meantempm'])
    return {'current_temp':current_temp,'current_cond':current_cond,'current_precip':current_precip,'history_high_temp':history_high_temp,'history_low_temp':history_low_temp}

def get_current_temp_data(city, city_short):
    format_city = '_'.join(city.title().split(' '))
    url = 'http://api.wunderground.com/api/%s/conditions/q/%s/%s.json' % (settings.WUNDERGROUND_KEY, city_short, format_city)
    r = requests.get(url)
    current_conditions_data = json.loads(r.text)
    return current_conditions_data

    

def get_current_conditions_and_history(lat,lng):
    #imperial units
    url = 'http://www.wunderground.com/cgi-bin/findweather/getForecast?query=%s,%s' % (lat,lng)
    r = requests.get(url)
    data = bs(r.text,'lxml')
    current_temp = format_temp(data.find_all('div',id='curTemp')[0].get_text().strip().split('\n')[0])
    current_cond = data.find_all('div', id='curCond')[0].get_text().strip()
    current_precip = data.find_all('span', attrs={"data-variable": "precip_today"})[0].get_text().strip().split('\n')[0]

    for x in data.find_all('a'):
        if x.has_attr('href'):
            t_url = x.get('href')
            if 'history' in t_url and 'monthlycalendar' in t_url.lower():
                n_url = 'http://www.wunderground.com/' + t_url
                n_r = requests.get(n_url)
                data_h = bs(n_r.text,'lxml')
                history_high, history_low = data_h.find_all('td',class_="todayBorder")[0].find_all('table', class_="dayTable")[1].find_all('tr')[2].get_text().strip().split('\n')[1].split('|')
                history_high_temp = format_temp(history_high)
                history_low_temp = format_temp(history_low)
                break
    return {'current_temp':current_temp,'current_cond':current_cond,'current_precip':current_precip,'history_high_temp':history_high_temp,'history_low_temp':history_low_temp}

def get_geo_coords_data(ip_address=None, user_agent=None):
    #bot usragent list to check against
    bots_user_agents = ['Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                        'Googlebot-Image/1.0', 
                        'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
                        'msnbot-media/1.1 (+http://search.msn.com/msnbot.htm)',
                        'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)'
    ]
    if user_agent not in bots_user_agents and 'bot' not in user_agent:
        # replace with freegeoip.net
        #geostring = 'https://maps.google.com/maps/api/geocode/json?address=%s&sensor=false' % (address)
        if ip_address == '127.0.0.1':
            geostring = 'http://freegeoip.net/json/'
        else:
            geostring = 'http://freegeoip.net/json/%s' % (ip_address)
        rgeo = requests.get(geostring, stream=False, headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.3'})
        geo = json.loads(rgeo.text)
        nationstate = geo['country_name']
        regionlocale = geo['region_name']
        ville = geo['city']
        lat = geo['latitude']
        lng = geo['longitude']
        coords = [lat,lng]
        return coords
    else:
        return None

def email_is_valid_format(email):
    if email == 'cinquemb@simple_weather_app.localhost':
        return True

    try:
        EmailField().clean(email)
        return True
    except ValidationError:
        return False

def format_email_address(address, name=None):
    if name:
        return '%s <%s>' % (name, address)
    else:
        return address

class EmailError(Exception):
    pass

class SendGridEmailer:
    def __init__(self):
        self.s = sendgrid.SendGridClient(settings.SENDGRID_KEY)

    def send_email(self,
            from_name,
            from_email,
            subject,
            html_body,
            to_emails,
            to_names=None,
            categories=None,
            plaintext_body=None,
            attachment_name=None,
            attachment_path=None):
        '''
        Send an email using sendgrid.
        from_name: name sending from
        from_email: email sending from
        to_emails: list of emails sending to
        to_names: list of names sending to,
            matching up with to_emails
        '''
        if from_name is None:
            raise EmailError('must supply from name')
        elif from_email is None:
            raise EmailError('must supply from name')
        elif not email_is_valid_format(from_email):
            raise EmailError('from email is not valid format %s' % from_email)
        for to_ in to_emails:
            if not email_is_valid_format(to_):
                raise EmailError('to email is not valid format %s' % from_email)

        if plaintext_body is None:
            plaintext_body = html2text.html2text(html_body)

        message = sendgrid.Mail()
        message.set_html(html_body)

        if from_email:
            message.set_from(from_email)

        if subject:
            message.set_subject(subject)

        if attachment_name and attachment_path:
            message.add_attachment(attachment_name, attachment_path)

        if to_names and to_emails:
            message.add_to(to_emails, to_names)
        elif to_emails:
            message.add_to(to_emails)

        if categories:
            message.add_category(categories)

        self.s.send(message)