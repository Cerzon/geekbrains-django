from django.shortcuts import render
from django.db.models import Count
from .models import ProductCategory, Product
from basketapp.models import UserBasket

def index(request):
    text_data = """С точки зрения банальной эрудиции
        не каждый локально мыслящий индивидуум
        способен утрировать теории физикоабстракции.

        Из жевательной резинки, килограммов из пяти, можно вылепить ботинки для последнего пути."""
    context_dict = {
        'page_title': 'Главная',
        'img_src': 'mainapp/img/main.jpg',
        'text_data': text_data,
    }
    return render(request, 'mainapp/index.html', context_dict)

def products(request, cat_tag=None, prod_tag=None):
    cat_list = ProductCategory.objects.all().annotate(num_prods=Count('products'))
    context_dict = {
        'errors': [],
        'page_title': 'товары',
        'img_src': 'mainapp/img/products.jpg',
        'categories': cat_list,
    }
    if request.session.get('basket_id', False):
        context_dict['basket'] = UserBasket.objects.filter(pk=request.session['basket_id'], state='active').first()
    cat_obj = None
    prod_obj = None
    if cat_tag:
        try:
            cat_obj = ProductCategory.objects.get(slug=cat_tag)
        except ProductCategory.DoesNotExist:
            cat_obj = None
            if not cat_tag == 'show-all':
                context_dict['errors'].append('(00| hA(k0R detected 1. Попытка зайти в несуществующую категорию товаров.')
    if prod_tag:
        if cat_obj:
            try:
                prod_obj = Product.objects.get(category=cat_obj, slug=prod_tag)
            except Product.DoesNotExist:
                prod_obj = None
                context_dict['errors'].append('(00| hA(k0R detected 2. Попытка найти несуществующий товар.')
        else:
            prod_obj = None
            context_dict['errors'].append('\/3Ry (00| hA(k0R detected. Даже категории такой нет, какой уж там может быть товар. Ходите уже по ссылкам, не морочьте голову.')
    prod_list = Product.objects.all()
    if prod_obj is None and cat_obj is None:
        context_dict['popular'] = prod_list.annotate(slot_num=Count('slots')).order_by('slot_num')[:3]
        if cat_tag == 'show-all': # all products list
            cat_title = 'Все товары'
        else: # products index
            return render(request, 'mainapp/products.html', context_dict)
    elif prod_obj: # product details
        context_dict['object'] = prod_obj
        return render(request, 'mainapp/product_detail.html', context_dict)
    else: # category product list
        prod_list = prod_list.filter(category=cat_obj)
        cat_title = cat_obj.name
        context_dict['popular'] = prod_list.annotate(slot_num=Count('slots')).order_by('slot_num')[:3]
    context_dict['object'] = prod_list
    context_dict['cat_title'] = cat_title
    return render(request, 'mainapp/products_list.html', context_dict)

def contacts(request):
    context_dict = {
        'page_title': 'Контакты',
        'img_src': 'img/contacts.jpg',
        'text_data': [
            'если б мишки были пчёлами,',
            'то они бы нипочём',
            'ни за что и не подумали',
            'так высоко строить дом.',
            'и тогда, конечно если бы',
            'пчёлы это были б мишки,',
            'нам бы, мишкам, не пришлось бы',
            'лазить на такие вышки.',
        ],
    }
    return render(request, 'mainapp/contacts.html', context_dict)