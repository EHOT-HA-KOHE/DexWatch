from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView

from users.forms import UserRegistrationForm, UserLoginForm
from watchlist.models import PoolList


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('main:index')

    # def get_success_url(self) -> str:
    #     redirect_page = self.request.POST.get('next')

    #     if redirect_page and redirect_page != reverse('user:logout'):
    #         return redirect_page
        
    #     return reverse_lazy('main:index')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.instance
        if user:
            form.save()
            auth.login(self.request, user)

            PoolList.objects.create(name='Favorites', user=user)

            messages.success(self.request, f'{user.username}, Вы успешно зарегистрированы и вошли в аккаунт')
            return HttpResponseRedirect(self.success_url)
    

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registration'
        return context
    

class UserProfileView(TemplateView):
    template_name = 'users/profile.html'


@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))
    