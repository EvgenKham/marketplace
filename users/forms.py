from django import forms
from django.contrib.auth.models import User

from users.models import Profile

status = (('Customer', 'Покупатель'), ('Seller', 'Продавец'), ('Customer/Seller', 'Покупатель/Продавец'))


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', )


class UserRegisterForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_check', 'email']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, *kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['email'].label = 'Эл. почта'
        self.fields['email'].help_text = 'Указывайте реальную почту'

    def save(self, commit=True):
        """
        Переопределил save, чтобы пароли сохранялись в хешированом виде.
        Если этого не сделать метод check_password из Loginform работает не корректно
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean(self):
        """Лучше каждую проверку определить в отдельный метод(single responsibility principle)"""
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Имя пользователя уже занято!')
        if password != password_check:
            raise forms.ValidationError('Ваши пароли не совпадают!')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с данной почтой уже существует!')


class ProfileRegisterForm(forms.ModelForm):
    status = forms.TypedChoiceField(label='Статус пользователя', choices=status)

    class Meta:
        model = Profile
        fields = ['status']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователя с данным именем не существует!')
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль! Попробуйте снова.')
