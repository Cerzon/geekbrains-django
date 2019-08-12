from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('<slug:cat_tag>/', mainapp.products, name='category'),
    path('<slug:cat_tag>/<slug:prod_tag>/', mainapp.products, name='product'),
]