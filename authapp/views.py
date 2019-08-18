from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

def login(request):
    return render(request, 'authapp/login.html')


def logout(request):
    return HttpResponseRedirect(reverse('index'))