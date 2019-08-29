from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser
from authapp.forms import ShopUserChangeForm, ShopUserRegisterForm


class SuperUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class CreateProductView(SuperUserPassesTestMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара'
        context['submit_label'] = 'Сохранить'
        context['links'] = {
            'list': ('adminapp:product_list', 'К перечню товаров',),
            'detail': ('adminapp:product_detail', 'Просмотр',),
            'create': ('adminapp:product_create', 'Создать новый',),
            'update': ('adminapp:product_update', 'Изменить',),
            'delete': ('adminapp:product_delete', 'Удалить',),
            'filter': ('adminapp:cat_product_list', 'По категории',),
        }
        return context

    def get_success_url(self):
        if self.object:
            return reverse_lazy('adminapp:product_detail', kwargs={'pk': self.object.pk})
        return super().get_success_url()


class UpdateProductView(SuperUserPassesTestMixin, UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование товара'
        context['submit_label'] = 'Применить изменения'
        context['links'] = {
            'list': ('adminapp:product_list', 'К перечню товаров',),
            'detail': ('adminapp:product_detail', 'Просмотр',),
            'create': ('adminapp:product_create', 'Создать новый',),
            'update': ('adminapp:product_update', 'Изменить',),
            'delete': ('adminapp:product_delete', 'Удалить',),
            'filter': ('adminapp:cat_product_list', 'По категории',),
        }
        return context
    
    def get_success_url(self):
        return reverse_lazy('adminapp:product_detail', kwargs={'pk': self.object.pk})


class DeleteProductView(SuperUserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'adminapp/object_delete.html'
    success_url = reverse_lazy('adminapp:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = {
            'list': ('adminapp:product_list', 'К перечню товаров',),
            'detail': ('adminapp:product_detail', 'Просмотр',),
            'create': ('adminapp:product_create', 'Создать новый',),
            'update': ('adminapp:product_update', 'Изменить',),
            'delete': ('adminapp:product_delete', 'Удалить',),
            'filter': ('adminapp:cat_product_list', 'По категории',),
        }
        return context


class ProductListView(SuperUserPassesTestMixin, ListView):
    model = Product
    template_name = 'adminapp/object_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs.get('category_id', False):
            queryset = queryset.filter(category__pk=self.kwargs['category_id'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.all()
        context['title'] = 'Товары'
        if self.kwargs.get('category_id', False):
            context['title'] += ' в категории "' + categories.get(pk=self.kwargs['category_id']).name + '"'
        context['filters'] = ProductCategory.objects.all()
        context['links'] = {
            'list': ('adminapp:product_list', 'К перечню товаров',),
            'detail': ('adminapp:product_detail', 'Просмотр',),
            'create': ('adminapp:product_create', 'Создать новый',),
            'update': ('adminapp:product_update', 'Изменить',),
            'delete': ('adminapp:product_delete', 'Удалить',),
            'filter': ('adminapp:cat_product_list', 'По категории',),
        }
        return context


class ProductDetailView(SuperUserPassesTestMixin, DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = {
            'list': ('adminapp:product_list', 'К перечню товаров',),
            'detail': ('adminapp:product_detail', 'Просмотр',),
            'create': ('adminapp:product_create', 'Создать новый',),
            'update': ('adminapp:product_update', 'Изменить',),
            'delete': ('adminapp:product_delete', 'Удалить',),
            'filter': ('adminapp:cat_product_list', 'По категории',),
        }
        return context


class CreateUserView(SuperUserPassesTestMixin, CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление пользователя'
        context['submit_label'] = 'Сохранить'
        context['links'] = {
            'list': ('adminapp:user_list', 'К списку пользователей',),
            'detail': ('adminapp:user_detail', 'Просмотр пользователя',),
            'create': ('adminapp:user_create', 'Создать пользователя',),
            'update': ('adminapp:user_update', 'Изменить пользователя',),
            'delete': ('adminapp:user_delete', 'Удалить пользователя',),
        }
        return context

    def get_success_url(self):
        if self.object:
            return reverse_lazy('adminapp:user_detail', kwargs={'pk': self.object.pk})
        return super().get_success_url()


class UpdateUserView(SuperUserPassesTestMixin, UpdateView):
    model = ShopUser
    form_class = ShopUserChangeForm
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование пользователя'
        context['submit_label'] = 'Применить изменения'
        context['links'] = {
            'list': ('adminapp:user_list', 'К списку пользователей',),
            'detail': ('adminapp:user_detail', 'Просмотр пользователя',),
            'create': ('adminapp:user_create', 'Создать пользователя',),
            'update': ('adminapp:user_update', 'Изменить пользователя',),
            'delete': ('adminapp:user_delete', 'Удалить пользователя',),
        }
        return context
    
    def get_success_url(self):
        return reverse_lazy('adminapp:user_detail', kwargs={'pk': self.object.pk})


class DeleteUserView(SuperUserPassesTestMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/object_delete.html'
    success_url = reverse_lazy('adminapp:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = {
            'list': ('adminapp:user_list', 'К списку пользователей',),
            'detail': ('adminapp:user_detail', 'Просмотр пользователя',),
            'create': ('adminapp:user_create', 'Создать пользователя',),
            'update': ('adminapp:user_update', 'Изменить пользователя',),
            'delete': ('adminapp:user_delete', 'Удалить пользователя',),
        }
        return context


class UserListView(SuperUserPassesTestMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/object_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        context['links'] = {
            'list': ('adminapp:user_list', 'К списку пользователей',),
            'detail': ('adminapp:user_detail', 'Просмотр пользователя',),
            'create': ('adminapp:user_create', 'Создать пользователя',),
            'update': ('adminapp:user_update', 'Изменить пользователя',),
            'delete': ('adminapp:user_delete', 'Удалить пользователя',),
        }
        return context


class UserDetailView(SuperUserPassesTestMixin, DetailView):
    model = ShopUser
    template_name = 'adminapp/user_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = {
            'list': ('adminapp:user_list', 'К списку пользователей',),
            'detail': ('adminapp:user_detail', 'Просмотр пользователя',),
            'create': ('adminapp:user_create', 'Создать пользователя',),
            'update': ('adminapp:user_update', 'Изменить пользователя',),
            'delete': ('adminapp:user_delete', 'Удалить пользователя',),
        }
        return context


class CreateCategoryView(SuperUserPassesTestMixin, CreateView):
    model = ProductCategory
    fields = '__all__'
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление категории'
        context['submit_label'] = 'Сохранить'
        context['links'] = {
            'list': ('adminapp:category_list', 'К списку категорий',),
            'detail': ('adminapp:category_detail', 'Просмотр категории',),
            'create': ('adminapp:category_create', 'Создать категорию',),
            'update': ('adminapp:category_update', 'Изменить категорию',),
            'delete': ('adminapp:category_delete', 'Удалить категорию',),
        }
        return context

    def get_success_url(self):
        if self.object:
            return reverse_lazy('adminapp:category_detail', kwargs={'pk': self.object.pk})
        return super().get_success_url()


class UpdateCategoryView(SuperUserPassesTestMixin, UpdateView):
    model = ProductCategory
    fields = '__all__'
    template_name = 'adminapp/object_update.html'
    success_url = reverse_lazy('adminapp:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование категории'
        context['submit_label'] = 'Применить изменения'
        context['links'] = {
            'list': ('adminapp:category_list', 'К списку категорий',),
            'detail': ('adminapp:category_detail', 'Просмотр категории',),
            'create': ('adminapp:category_create', 'Создать категорию',),
            'update': ('adminapp:category_update', 'Изменить категорию',),
            'delete': ('adminapp:category_delete', 'Удалить категорию',),
        }
        return context
    
    def get_success_url(self):
        return reverse_lazy('adminapp:category_detail', kwargs={'pk': self.object.pk})


class DeleteCategoryView(SuperUserPassesTestMixin, DeleteView):
    model = ProductCategory
    template_name = 'adminapp/object_delete.html'
    success_url = reverse_lazy('adminapp:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = {
            'list': ('adminapp:category_list', 'К списку категорий',),
            'detail': ('adminapp:category_detail', 'Просмотр категории',),
            'create': ('adminapp:category_create', 'Создать категорию',),
            'update': ('adminapp:category_update', 'Изменить категорию',),
            'delete': ('adminapp:category_delete', 'Удалить категорию',),
        }
        return context


class CategoryListView(SuperUserPassesTestMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/object_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        context['links'] = {
            'list': ('adminapp:category_list', 'К списку категорий',),
            'detail': ('adminapp:category_detail', 'Просмотр категории',),
            'create': ('adminapp:category_create', 'Создать категорию',),
            'update': ('adminapp:category_update', 'Изменить категорию',),
            'delete': ('adminapp:category_delete', 'Удалить категорию',),
        }
        return context


class CategoryDetailView(SuperUserPassesTestMixin, DetailView):
    model = ProductCategory
    template_name = 'adminapp/category_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = {
            'list': ('adminapp:category_list', 'К списку категорий',),
            'detail': ('adminapp:category_detail', 'Просмотр категории',),
            'create': ('adminapp:category_create', 'Создать категорию',),
            'update': ('adminapp:category_update', 'Изменить категорию',),
            'delete': ('adminapp:category_delete', 'Удалить категорию',),
        }
        return context
