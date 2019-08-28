from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from mainapp.models import Product, ProductCategory


class CreateProductView(CreateView):
    pass


class UpdateProductView(UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'adminapp/product_update.html'
    success_url = reverse_lazy('adminapp:product_list')

    def get_success_url(self):
        return reverse_lazy('adminapp:product_detail', kwargs={'pk': self.kwargs['pk']})


class DeleteProductView(DeleteView):
    pass


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/product_list.html'

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
        context['categories'] = ProductCategory.objects.all()
        return context
    


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'
