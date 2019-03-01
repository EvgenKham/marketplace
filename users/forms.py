from django import forms
from django.contrib.auth.models import User

from users.models import Profile

status = (('Customer', 'Покупатель'), ('Seller', 'Продавец'), ('Customer/Seller', 'Покупатель/Продавец'))


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', )


class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'status', ]

    name = forms.CharField(max_length=128, label='Логин',
                           help_text='Обязательное поле. Только буквы, цифры и символы @/./+/-/_.',
                           error_messages={'required': 'Введите ваш логин'})
    email = forms.EmailField(label='Эл. почта', help_text='Указывайте реальную почту')
    status = forms.TypedChoiceField(label='Статус пользователя', choices=status)

    def clean(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        if Profile.objects.filter(name=name).exists():
            raise forms.ValidationError('Пользователь с данным именем уже существует!')
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с данной почтой уже существует!')


class LoginForm(forms.Form):
    name = forms.CharField(max_length=128)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Логин'
        self.fields['email'].label = 'Эл. почта'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        # name = self.cleaned_data['name']
        # email = self.cleaned_data['email']
        if not Profile.objects.filter(name=name).exists():
            raise forms.ValidationError('Пользователя с данным именем не существует!')
        if not Profile.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователя с данной почтой не существует!')
