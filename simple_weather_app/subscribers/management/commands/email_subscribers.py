from django.core.management.base import BaseCommand, CommandError
from subscribers.utils import send_email_confirmation
from subscribers.models import WeatherSubscriber
import csv
import os

COMPANY_CSV = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), '_amenities.csv')

class Command(BaseCommand):
    args = '<path to csv file>'
    help = 'parses a csv file and populates the db with amenities'

    def handle(self, *args, **options):
        company_fname = args[0] if len(args) > 0 else COMPANY_CSV

        csvfile = open(company_fname, 'U')
        reader = csv.DictReader(csvfile)
        for d in reader:
            name = d['types']
            amenity, created = Amenity.objects.get_or_create(normalized_name=Amenity.get_normalized_name(name),defaults={'name': name})
            print amenity.name