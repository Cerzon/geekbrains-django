from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.db.models import F
from .models import UserBasket, BasketSlot
from mainapp.models import Product
from authapp.models import ShopUser


def index(request):
    slots = list()
    if request.session.get('basket_id', False):
        slots = BasketSlot.objects.filter(
            basket__pk=request.session['basket_id'],
            basket__state='active'
        ).select_related('product')
    context_dict = {
        'slots': slots,
        'basket_id': request.session.get('basket_id', None),
    }
    return render(request, 'basketapp/basket_detail.html', context_dict)


def add_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.session.get('basket_id', False):
        try:
            basket = UserBasket.objects.get(pk=request.session['basket_id'])
        except UserBasket.DoesNotExist:
            basket = UserBasket()
    else:
        basket = UserBasket()
    if request.user.is_authenticated:
        if not basket.customer == request.user:
            basket = UserBasket()
        basket.customer = request.user
    basket.save()
    request.session['basket_id'] = basket.pk
    basket_slot, created = basket.slots.get_or_create(basket=basket, product=product)
    if not created:
        basket_slot.quantity = F('quantity') + 1
    basket_slot.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if not request.session.get('basket_id', False):
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        try:
            basket = UserBasket.objects.get(pk=request.session['basket_id'])
        except UserBasket.DoesNotExist:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if request.user.is_authenticated:
        if not basket.customer == request.user:
            del request.session['basket_id']
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        basket.customer = request.user
        basket.save()
    else:
        if basket.customer:
            del request.session['basket_id']
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    try:
        basket_slot = basket.slots.get(basket=basket, product=product)
    except BasketSlot.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    basket_slot.quantity -= 1
    if not basket_slot.quantity:
        basket_slot.delete()
    else:
        basket_slot.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def clear_basket(request, basket_id):
    BasketSlot.objects.filter(basket__pk=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def drop_basket(request, basket_id):
    pass


def update_slot(request, slot_slug):
    slot_id = int(slot_slug.split('_')[0])
    try:
        basket_slot = BasketSlot.objects.get(pk=slot_id)
    except BasketSlot.DoesNotExist:
        return HttpResponse('что-то пошло не так - обновлять нечего')
    quantity = request.GET.get('quantity', False)
    if quantity:
        basket_slot.quantity = quantity
        basket_slot.save()
    return HttpResponse('slot updated')


def delete_slot(request, slot_slug):
    slot_id = int(slot_slug.split('_')[-1])
    try:
        basket_slot = BasketSlot.objects.get(pk=slot_id)
    except BasketSlot.DoesNotExist:
        return HttpResponse('что-то пошло не так - удалять нечего')
    basket_slot.delete()
    return HttpResponse('slot deleted')
