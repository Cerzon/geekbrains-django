from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.index, name='index'),
    path('add/<slug:cat_tag>/<slug:prod_tag>/', basketapp.add_product, name='add_product'),
    path('remove/<slug:cat_tag>/<slug:prod_tag>/', basketapp.remove_product, name='remove_product'),
    path('clear/<int:pk>/', basketapp.clear_basket, name='clear_basket'),
    path('drop/<int:pk>/', basketapp.drop_basket, name='drop_basket'),
]