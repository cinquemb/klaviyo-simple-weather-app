from django.conf import settings
from django.forms import EmailField
from django.core.exceptions import ValidationError
import sendgrid
import urllib
import urllib2
import html2text

def get_current_temp():
    'http://api.wunderground.com/api/751b945b05e70eb6/conditions/q/CA/San_Francisco.json'
    pass

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
        geostring = 'http://freegeoip.net/json/%s' % (ip_address)
        rgeo = requests.get(geostring, stream=False, headers={'User-Agent':' Mozilla/4.0 (Macintosh; Intel Mac OS X 10.6; rv:21.0) Gecko/20100104 Firefox/20.0'})
        geo = json.loads(rgeo.text)
        nationstate = geo['country_name']
        regionlocale = geo['region_name']
        ville = geo['city']
        lat = geo['latitude']
        lng = geo['longitude']
        coords = 'lat:%s,lng:%s' % (lat,lng)
        return coords
    else:
        return None

def email_is_valid_format(email):
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
        self.s = sendgrid.Sendgrid(
            settings.SENDGRID_USER,
            settings.SENDGRID_PASS,
            secure=True)

    def send_email(self,
            from_name,
            from_email,
            subject,
            html_body,
            to_emails,
            to_names,
            categories=None,
            plaintext_body=None,
            attachment_name=None,
            attachment_path=None,
            subscription_track=True):
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

        message = sendgrid.Message(
            (from_email, from_name),
            subject,
            plaintext_body,
            html_body,
        )
        if attachment_name and attachment_path:
            message.add_attachment(attachment_name, attachment_path)
        if not subscription_track:
            message.add_filter_setting('subscriptiontrack', 'enable', 0)
        message.add_to(to_emails, to_names)

        if categories:
            message.add_category(categories)

        self.s.web.send(message)