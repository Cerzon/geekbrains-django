import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-d', '--data', default='data_input.json', type=str)

    def handle(self, *args, **options):
        with open(os.path.join(settings.MEDIA_ROOT, 'data', options['data']), 'r', encoding='utf-8') as data_file:
            try:
                categories = json.load(data_file)['categories']
            except json.JSONDecodeError:
                categories = None
            try:
                users = json.load(data_file)['users']
            except json.JSONDecodeError:
                users = None
        if categories:
            for category in categories:
                cat_obj, created = ProductCategory.objects.get_or_create(
                    slug=category['slug'],
                    defaults={'name': category['name']},
                )
                cat_obj.save()
                for prod in category['products']:
                    prod_obj, created = Product.objects.get_or_create(
                        category=cat_obj,
                        slug=prod['slug'],
                        defaults={'name': prod['name'], 'price': prod['price']},
                    )
                    prod_obj.save()
        if users:
            for user in users:
                pass
        else:
            ShopUser.objects.all().delete()
            ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=41)
