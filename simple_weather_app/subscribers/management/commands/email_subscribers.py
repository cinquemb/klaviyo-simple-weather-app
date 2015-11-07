from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.test.client import RequestFactory
from django.core.handlers.base import BaseHandler  
from django.conf import settings

from subscribers.utils import send_email_confirmation
from subscribers.models import WeatherSubscriber

class MiddlewareRequestFactory(RequestFactory):
    def request(self, **request):  
        "Construct a generic request object."  
        request = RequestFactory.request(self, **request)  
        handler = BaseHandler()  
        handler.load_middleware()  
        for middleware_method in handler._request_middleware:  
            if middleware_method(request):  
                raise Exception("Couldn't create request mock object - "  
                                "request middleware returned a response")  
        return request  

class Command(BaseCommand):
    help = 'email bus companies notifying them to claim their profile'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.request_factory = MiddlewareRequestFactory(
                SERVER_NAME=settings.SERVER_NAME)

    def claim_profile(self, company):
        user = company.user
        email = EmailAddress.objects.filter(user=user)
        if email:
            email = email[0]
        request = self.request_factory.get('/')
        send_email_confirmation(request, user, company=company)
        print 'sent confirmation for email: %s' % (email)

    def get_companies(self):
        return Company.objects.all()

    def handle(self, *args, **options):
        for company in self.get_companies():
            self.claim_profile(company)
