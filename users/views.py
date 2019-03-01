from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.views.generic.edit import FormView
from django.views.generic.base import View

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse

from users.forms import ProfileRegisterForm, LoginForm, ProfileEditForm

from users.models import Profile
from users.authentication import EmailAuthBackend


class LogoutView(View):
    """Класс для выхода из учетной записи"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
        pass


# class LoginFormView(FormView):
#     """Класс для авторизации пользователей"""
#     form_class = AuthenticationForm
#     template_name = "login.html"
#     success_url = "/"
#
#     def form_valid(self, form):
#         self.user = form.get_user()
#         login(self.request, self.user)
#         return super(LoginFormView, self).form_valid(form)
#         pass


def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        login_user = authenticate(username=name, email=email)
        if login_user:
            # login(request, login_user)
            return redirect('/')
    return render(request, 'login.html', {'login_form': form})


# class UserRegistrationForm(FormView):
#     """Класс для регистрации новых пользователей"""
#     form_class = UserRegisterForm
#     template_name = "register.html"
#     success_url = "/user/login/"
#
#     def form_valid(self, form):
#         form.save()
#         return super(UserRegistrationForm, self).form_valid(form)
#         pass


def register(request):
    if request.method == 'POST':
        form = ProfileRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user/login/')
        # else:
        #     form = ProfileRegisterForm()
        return render(request, 'register.html', {'user_form': form})
    else:
        form = ProfileRegisterForm()
        return render(request, 'register.html', {'user_form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(data=request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            # return redirect('settings:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'users/edit.html',
                      {'profile_form': profile_form})

