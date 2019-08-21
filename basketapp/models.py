from django.db import models
from django.db.models import Sum, Count, F
from mainapp.models import Product
from authapp.models import ShopUser


class UserBasket(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    customer = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket', verbose_name='покупатель')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return 'Корзина пользователя {0} от {1}'.format(self.customer.username or 'Аноним', self.created.strftime('%d %b %Y'))

    def basket_info(self):
        return self.slot.aggregate(
            total=Sum(
                F('product__price') * F('quantity'),
                output_field=models.DecimalField()),
            product_num=Count('pk'),
            quantity_total=Sum('quantity')
        )


class BasketSlot(models.Model):
    basket = models.ForeignKey(UserBasket, on_delete=models.CASCADE, related_name='slot', verbose_name='корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='slot', verbose_name='товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default=1)

    class Meta:
        verbose_name = 'слот корзины'
        verbose_name_plural = 'слоты корзины'
        ordering = ['basket',]

    def __str__(self):
        return '({0}) {1} - {2}'.format(self.basket.customer.username or 'Аноним', self.product.name, self.quantity)
