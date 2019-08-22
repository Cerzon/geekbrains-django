from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.index, name='index'),
    path('add/<int:product_id>/', basketapp.add_product, name='add_product'),
    path('remove/<int:product_id>/', basketapp.remove_product, name='remove_product'),
    path('clear/<int:basket_id>/', basketapp.clear_basket, name='clear_basket'),
    path('drop/<int:basket_id>/', basketapp.drop_basket, name='drop_basket'),
]