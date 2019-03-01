from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.views.generic.edit import FormView
from django.views.generic.base import View

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse

from users.forms import UserRegisterForm, ProfileRegisterForm, LoginForm, ProfileEditForm

from users.models import Profile


class LogoutView(View):
    """Класс для выхода из учетной записи"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
        pass


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def register(request):
    """
    Форма регистрации является составной(UserRegisterForm и ProfileRegisterForm).
    По-этому после валидации сохраняется User, а только потом создается Profile
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            profile.status = profile_form.cleaned_data['status']
            profile.save()
            return redirect('/user/login/')
        return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
        return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


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

