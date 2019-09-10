from django.contrib import admin
from .models import ProductCategory, Product, DataInput


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'name',
        'slug',
    )
    list_display_links = (
        '__str__',
    )
    list_editable = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    fields = (
        ('name', 'slug',),
        'description',
    )
    
admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'name',
        'slug',
        'category',
    )
    list_display_links = (
        '__str__',
    )
    list_editable = (
        'name',
        'slug',
        'category',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_filter = (
        'category',
    )
    fields = (
        ('name', 'slug', 'category',),
        'image',
        'description'
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(DataInput)
