from django.utils.functional import cached_property
from django.db import models
from django.db.models import Sum, Count, F
from mainapp.models import Product
from authapp.models import ShopUser


class UserBasket(models.Model):
    STATE_CHOICES = (
        ('active', 'Активная',),
        ('chkout', 'Оформлен заказ',),
        ('droped', 'Брошенная',),
        ('delete', 'Удалённая',),
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    customer = models.ForeignKey(ShopUser, on_delete=models.CASCADE, null=True, related_name='basket', verbose_name='покупатель')
    state = models.CharField(max_length=6, choices=STATE_CHOICES, default='active', verbose_name='статус корзины')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        username = 'anonymous'
        if self.customer:
            username = self.customer.username
        return 'Корзина пользователя {0} от {1}'.format(username, self.created.strftime('%d %b %Y'))

    @cached_property
    def get_info(self):
        return self.slots.aggregate(
            total=Sum(
                F('product__price') * F('quantity'),
                output_field=models.DecimalField()),
            product_num=Count('pk'),
            quantity_total=Sum('quantity')
        )


class BasketSlot(models.Model):
    basket = models.ForeignKey(UserBasket, on_delete=models.CASCADE, related_name='slots', verbose_name='корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='slots', verbose_name='товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default=1)

    class Meta:
        verbose_name = 'слот корзины'
        verbose_name_plural = 'слоты корзины'
        ordering = ['basket',]

    def __str__(self):
        username = 'anonymous'
        if self.basket.customer:
            username = self.basket.customer.username
        return '({0}) {1} - {2}'.format(username, self.product.name, self.quantity)

    @property
    def cost(self):
        return self.product.price * self.quantity


class UserOrder(UserBasket):
    class Meta:
        proxy = True
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return 'Заказ пользователя {0} от {1}'.format(self.customer.username, self.created.strftime('%d %b %Y'))
