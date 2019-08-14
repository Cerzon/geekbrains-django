from django.shortcuts import render
from .models import ProductCategory, Product

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
    context_dict = {
        'page_title': 'Продукты',
        'img_src': 'mainapp/img/products.jpg',
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
    return render(request, 'mainapp/products.html', context_dict)

def contacts(request):
    with open('media/data/contacts.json', 'r', encoding='utf-8') as data_file:
        context_dict = json.load(data_file)
    return render(request, 'mainapp/contacts.html', context_dict)