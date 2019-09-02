from django.contrib import admin
from .models import UserBasket, BasketSlot, UserOrder


class BasketSlotInline(admin.StackedInline):
    model = BasketSlot
    extra = 0
    readonly_fields = ('cost',)
    fields = (
        ('product', 'quantity', 'cost',),
    )

    def cost(self, obj):
        return obj.product.price * obj.quantity

    cost.short_description = 'Стоимость'


class BasketAdmin(admin.ModelAdmin):
    inlines = [
        BasketSlotInline,
    ]
    readonly_fields = (
        'customer',
        'basket_number',
        'basket_total',
    )
    fields = (
        ('customer', 'basket_number', 'basket_total',),
    )
    save_on_top = True

    def basket_total(self, obj):
        total = obj.get_info['total']
        if not total:
            total = 0
        return '{:.2f}'.format(total)

    def basket_number(self, obj):
        return '#{0} от {1}'.format(obj.pk, obj.created.strftime('%d %b %Y'))


class UserBasketAdmin(BasketAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(state='chkout')
        return queryset

    def basket_total(self, obj):
        return super().basket_total(obj)

    def basket_number(self, obj):
        return super().basket_number(obj)

    basket_total.short_description = 'Сумма корзины итого'
    basket_number.short_description = 'Номер корзины'

admin.site.register(UserBasket, UserBasketAdmin)


class UserOrderAdmin(BasketAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(state='chkout')
        return queryset

    def basket_total(self, obj):
        return super().basket_total(obj)

    def basket_number(self, obj):
        return super().basket_number(obj)

    basket_total.short_description = 'Сумма заказа итого'
    basket_number.short_description = 'Номер заказа'

admin.site.register(UserOrder, UserOrderAdmin)
