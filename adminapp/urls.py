from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('products/list/', adminapp.ProductListView.as_view(), name='product_list'),
    path('products/list/category/<int:category_id>/', adminapp.ProductListView.as_view(), name='cat_product_list'),
    path('products/detail/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', adminapp.CreateProductView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', adminapp.UpdateProductView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', adminapp.DeleteProductView.as_view(), name='product_delete'),
]