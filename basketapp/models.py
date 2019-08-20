from django.db import models
from mainapp.models import Product
from authapp.models import ShopUser


class UserBasket(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    customer = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket', verbose_name='покупатель')


class BasketSlot(models.Model):
    basket = models.ForeignKey(UserBasket, on_delete=models.CASCADE, related_name='slot', verbose_name='корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='slot', verbose_name='товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='количество')
