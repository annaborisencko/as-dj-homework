import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            # TODO: Добавьте сохранение модели
            id = phone['id']
            name = phone['name']
            image = phone['image']
            price = phone['price']
            release_date = phone['release_date']
            lte_exists = phone['lte_exists']

            #Формируем слаггированное название телефона
            name_for_slug = name.lower()
            brend = name_for_slug.split()[0]
            series = name_for_slug.split()[len(name.split())-1]
            model_full = name_for_slug.split()[1:-1]
            model = '-'
            if model_full != '':
                for word in model_full:
                    model += word[0]
            slug = f"{brend}{model}{series}"
            Phone.objects.create(
                id = id, 
                name = name, 
                image = image, 
                price = price, 
                release_date = release_date, 
                lte_exists = lte_exists,
                slug = slug,
                )
