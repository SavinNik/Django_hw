import csv
from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    help = 'Import phones from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            phone_instance = Phone(
                name=phone['name'],
                price=phone['price'],
                image=phone['image'],
                release_date=phone['release_date'],
                lte_exists=phone['lte_exists'].lower() == 'true'
            )
            phone_instance.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported phones'))
