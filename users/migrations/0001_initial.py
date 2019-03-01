# Generated by Django 2.1.7 on 2019-03-01 12:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, default='photos/unknown_user.jpg', upload_to='photos/%Y_%m/%d', verbose_name='Фото')),
                ('status', models.CharField(max_length=32, verbose_name='Статус')),
                ('account', models.DecimalField(blank=True, decimal_places=2, default=100.0, max_digits=10, verbose_name='Счет')),
                ('user', models.OneToOneField(blank=True, default='0000000', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Посетитель',
                'verbose_name_plural': 'Посетители',
                'ordering': ['id', 'user', 'account'],
            },
        ),
        migrations.AlterIndexTogether(
            name='profile',
            index_together={('id', 'user')},
        ),
    ]
