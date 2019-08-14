import os, json
from django.db import models
from django.conf import settings

class ProductCategory(models.Model):
    slug = models.SlugField(max_length=30, unique=True, verbose_name='имя для URL-а')
    name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.TextField(blank=True, verbose_name='описание')

    class Meta:
        verbose_name = 'категория товаров'
        verbose_name_plural = 'категории товаров'
        ordering = ['name',]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория', related_name='products')
    slug = models.SlugField(max_length=30, verbose_name='имя для URL-а')
    name = models.CharField(max_length=220, verbose_name='наименование')
    image = models.ImageField(upload_to='products_img', blank=True, verbose_name='фотография товара')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='цена')
    stock = models.PositiveSmallIntegerField(default=0, verbose_name='остаток на складе')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        unique_together = ('category', 'slug',)
        ordering = ['category', 'name',]

    def __str__(self):
        return '{0} :: {1}'.format(self.category.name, self.name)


class DataInput(models.Model):
    data_file = models.FileField(upload_to='data')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with open(os.path.join(settings.MEDIA_ROOT, self.data_file), 'r', encoding="utf-8") as data_input:
            data_list = json.load(data_input)['categories']
        for category in data_list:
            cat_obj, created = ProductCategory.objects.get_or_create(
                slug=category['slug'],
                defaults={'name': category['name']},
            )
            cat_obj.save()
            for prod in category['products']:
                prod_obj, created = Product.objects.get_or_create(
                    category=cat_obj,
                    slug=prod['slug'],
                    defaults={'name': prod['name'], 'price': prod['price']},
                )
                prod_obj.save()
