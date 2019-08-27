from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.index, name='index'),
    path('add/<int:product_id>/', basketapp.add_product, name='add_product'),
    path('remove/<int:product_id>/', basketapp.remove_product, name='remove_product'),
    path('update/<slug:slot_slug>/', basketapp.update_slot, name='update_slot'),
    path('delete/<slug:slot_slug>/', basketapp.delete_slot, name='delete_slot'),
    path('clear/<int:basket_id>/', basketapp.clear_basket, name='clear_basket'),
    # path('drop/<int:basket_id>/', basketapp.drop_basket, name='drop_basket'),
    path('checkout/<int:basket_id>/', basketapp.checkout, name='checkout'),
    path('confirm/<int:order_id>/', basketapp.confirm_order, name='confirm_order'),
]