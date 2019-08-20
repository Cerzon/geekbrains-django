from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import UserBasket, BasketSlot
from mainapp.models import Product
from authapp.models import ShopUser


def index(request):
    pass


def add_product(request, cat_tag, prod_tag):
    pass


def remove_product(request, cat_tag, prod_tag):
    pass


def clear_basket(request, basket_id):
    pass


def drop_basket(request, basket_id):
    pass