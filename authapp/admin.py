from django.contrib import admin
from django.db.models import Count, F, Sum, DecimalField
from .models import ShopUser
from basketapp.models import UserBasket, UserOrder


class UserBasketsInline(admin.StackedInline):
    ordering = ('-created',)
    extra = 0
    readonly_fields = ('basket_total',)
    show_change_link = True

    def has_add_permission(self, request):
        return False

    def basket_total(self, obj):
        total = obj.get_info['total']
        if not total:
            total = 0
        return '{:.2f}'.format(total)

    basket_total.short_description = 'Сумма итого'


class UserBasketInline(UserBasketsInline):
    model = UserBasket
    fields = (
        ('state', 'basket_total',),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(state='chkout')
        return queryset


class UserOrderInline(UserBasketsInline):
    model = UserOrder
    fields = (
        'basket_total',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(state='chkout')
        return queryset


class ShopUserAdmin(admin.ModelAdmin):
    inlines = [
        UserBasketInline,
        UserOrderInline,
    ]
    list_display = (
        '__str__',
        'basket_num',
        'order_num',
    )
    save_on_top = True

    def basket_num(self, obj):
        return obj.basket.exclude(state='chkout').count()

    basket_num.short_description = 'Корзин набрано'

    def order_num(self, obj):
        return obj.basket.filter(state='chkout').count()

    order_num.short_description = 'Заказов оформлено'


admin.site.register(ShopUser, ShopUserAdmin)
