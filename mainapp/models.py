from django.db import models

class ProductCategory(models.Model):
    slug = models.SlugField(max_length=30, unique=True, verbose_name='имя для URL-а')
    name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.TextField(blank=True, verbose_name='описание')

    class Meta():
        verbose_name = 'категория товаров'
        verbose_name_plural = 'категории товаров'
        ordering = ['name',]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, verbose_name='категория', related_name='products')
    slug = models.SlugField(max_length=30, verbose_name='имя для URL-а')
    name = models.CharField(max_length=220, verbose_name='наименование')
    image = models.ImageField(upload_to='products_img', blank=True, verbose_name='фотография товара')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='цена')
    stock = models.PositiveSmallIntegerField(default=0, verbose_name='остаток на складе')

    class Meta():
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        unique_together = ('category', 'slug',)
        ordering = ['category', 'name',]

    def __str__(self):
        return '{0} :: {1}'.format(self.category.name, self.name)
