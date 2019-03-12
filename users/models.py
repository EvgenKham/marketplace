from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, default="0000000")
    photo = models.ImageField(verbose_name='Фото', upload_to='photos/%Y_%m/%d', blank=True,
                              default='photos/default_user.jpg')
    account = models.DecimalField(verbose_name='Счет', max_digits=10, decimal_places=2, default=100.00, blank=True)

    class Meta:
        ordering = ['id', 'user', 'account']
        index_together = [
            ['id', 'user']
        ]
        verbose_name = 'Посетитель'
        verbose_name_plural = 'Посетители'

    def __str__(self):
        return self.user.username

    def get_get_absolute_url(self):
        return reverse('user:detail', kwargs={'user': self.user.username})
