from django.contrib import admin
from django.db.models import Count, F, Sum, DecimalField
from .models import ShopUser
from basketapp.models import UserBasket


class UserBasketInline(admin.StackedInline):
    model = UserBasket
    ordering = ('-created',)
    extra = 0
    readonly_fields = ('basket_total',)
    fields = (
        ('state', 'basket_total',),
    )
    show_change_link = True

    def has_add_permission(self, request):
        return False

    def basket_total(self, obj):
        basket = obj.slots.aggregate(total=Sum(
            F('product__price') * F('quantity'),
            output_field=DecimalField())
        )
        if not basket['total']:
            basket['total'] = 0
        return '{:.2f}'.format(basket['total'])

    basket_total.short_description = 'Сумма итого'


class ShopUserAdmin(admin.ModelAdmin):
    inlines = [
        UserBasketInline,
    ]
    list_display = (
        '__str__',
        'basket_num',
        'order_num',
    )
    save_on_top = True

    def basket_num(self, obj):
        return obj.basket.exclude(state='chkout').count()

    def order_num(self, obj):
        return obj.basket.filter(state='chkout').count()


admin.site.register(ShopUser, ShopUserAdmin)
