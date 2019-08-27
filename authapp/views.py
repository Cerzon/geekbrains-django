from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView, FormView
from .models import ShopUser
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserChangeForm
from basketapp.models import UserBasket


class UserLoginView(FormView):
    template_name = 'authapp/login.html'
    form_class = ShopUserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        auth.login(self.request, user)
        if self.request.session.get('basket_id', False):
            try:
                basket = UserBasket.objects.get(pk=self.request.session['basket_id'], state='active')
            except UserBasket.DoesNotExist:
                del self.request.session['basket_id']
            else:
                if not basket.customer:
                    basket.customer = user
                    basket.save()
            if basket.customer != user:
                del self.request.session['basket_id']
        else:
            basket = UserBasket.objects.filter(
                customer=user,
                state='active',
                created__gt=datetime.today() - timedelta(days=10)
            ).order_by('-created').first()
            if basket:
                self.request.session['basket_id'] = basket.pk
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['next'] = self.request.GET.get('next', None)
        elif self.request.method == 'POST':
            context['next'] = self.request.POST.get('next', None)
        return context

    def get_success_url(self):
        if self.request.POST.get('next', False):
            return self.request.POST['next']
        return super().get_success_url()


def logout(request):
    if request.session.get('basket_id', False):
        del request.session['basket_id']
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
