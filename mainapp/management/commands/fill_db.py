import os
import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mainapp.models import ProductCategory, Product
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass