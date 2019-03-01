from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя пользователя', unique=True,
                            help_text='Только буквы, цифры и @ /. / + / - / _. ',)
    email = models.EmailField(verbose_name='Почта', unique=True)
    user = models
    photo = models.ImageField(verbose_name='Фото', upload_to='photos/%Y_%m/%d', blank=True,
                              default='photos/unknown_user.jpg')
    status = models.CharField(max_length=32, verbose_name='Статус')
    account = models.DecimalField(verbose_name='Счет', max_digits=10, decimal_places=2, default=100.00, blank=True)

    class Meta:
        ordering = ['id', 'name', 'account']
        index_together = [
            ['id', 'name']
        ]
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'

    def __str__(self):
        return self.name

    def get_get_absolute_url(self):
        return reverse('user:detail', kwargs={'user': self.name})

    def check_email(self, email):
        if self.email == email:
            return True
        else:
            return False
