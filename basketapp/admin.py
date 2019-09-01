from django.contrib import admin
from .models import UserBasket, BasketSlot


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


class UserBasketAdmin(admin.ModelAdmin):
    inlines = [
        BasketSlotInline,
    ]
    save_on_top = True


admin.site.register(UserBasket, UserBasketAdmin)
