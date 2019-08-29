from django.urls import path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('users/list/', adminapp.UserListView.as_view(), name='user_list'),
    path('users/detail/<int:pk>/', adminapp.UserDetailView.as_view(), name='user_detail'),
    path('users/create/', adminapp.CreateUserView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', adminapp.UpdateUserView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', adminapp.DeleteUserView.as_view(), name='user_delete'),
    path('products/list/', adminapp.ProductListView.as_view(), name='product_list'),
    path('products/list/category/<int:category_id>/', adminapp.ProductListView.as_view(), name='cat_product_list'),
    path('products/detail/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_detail'),
    path('products/create/', adminapp.CreateProductView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', adminapp.UpdateProductView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', adminapp.DeleteProductView.as_view(), name='product_delete'),
    path('categories/list/', adminapp.CategoryListView.as_view(), name='category_list'),
    path('categories/detail/<int:pk>/', adminapp.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/create/', adminapp.CreateCategoryView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', adminapp.UpdateCategoryView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.DeleteCategoryView.as_view(), name='category_delete'),
]