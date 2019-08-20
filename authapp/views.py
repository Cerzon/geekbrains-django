from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, FormView
from .models import ShopUser
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserChangeForm


class UserLoginView(FormView):
    template_name = 'authapp/login.html'
    form_class = ShopUserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        auth.login(self.request, user)
        return super().form_valid(form)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
    
        if register_form.is_valid():
            user = register_form.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        register_form = ShopUserRegisterForm()
    context_dict = {
        'page_title': 'регистрация',
        'form': register_form,
    }
    return render(request, 'authapp/register.html', context_dict)


class EditUserProfileView(UpdateView):
    template_name = 'authapp/edit.html'
    form_class = ShopUserChangeForm
    model = ShopUser
    success_url = reverse_lazy('index')
