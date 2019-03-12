from django.views.generic.base import View

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from users.forms import UserRegisterForm, ProfileRegisterForm, LoginForm, UserEditForm, ProfileEditForm

from users.models import Profile
from cart.models import Cart
from orders.models import Order, OrderItem


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


def register_view(request):
    """
    Форма регистрации является составной(UserRegisterForm и ProfileRegisterForm).
    По-этому после валидации сохраняется User, а только потом создается Profile
    """
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            profile = Profile.objects.create(user=new_user)

            avatar = request.FILES.get('photo')
            if avatar:
                profile.photo = avatar

            profile.save()
            return redirect('/user/login/')
        return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
        return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})


def account_view(request):
    user = User.objects.get(username=request.user)
    cart = Cart(request)
    order = Order.objects.filter(customer=user.username).last()
    order_items = OrderItem.objects.filter(order_id=order.id)
    context = {'user': user,
               'cart': cart,
               'order': order,
               'order_items': order_items}
    return render(request, 'account.html', context)


@login_required
def edit_view(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            change_user = user_form.save(commit=False)
            change_user.save()
            profile = Profile.objects.get(user=change_user)
            avatar = request.FILES.get('photo')
            if avatar:
                profile.photo = avatar
            profile_form.save()
            return redirect('users:account')
        return request(request, 'edit.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'edit.html', {'user_form': user_form,
                                             'profile_form': profile_form})
