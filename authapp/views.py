from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from .forms import ShopUserLoginForm, ShopUserRegisterForm

def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    context_dict = {
        'page_title': 'вход',
        'form': login_form,
    }
    return render(request, 'authapp/login.html', context_dict)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
    
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
    context_dict = {
        'pate_title': 'регистрация',
        'form': register_form,
    }
    return render(request, 'authapp/register.html', context_dict)


def edit(request, user_id):
    return HttpResponseRedirect(reverse('index'))
