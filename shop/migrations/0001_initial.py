# Generated by Django 2.1.7 on 2019-03-01 12:37

from django.db import migrations, models
import django.db.models.deletion
import shop.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, verbose_name='Категория')),
                ('slug', models.SlugField(blank=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('icon', models.ImageField(blank=True, default='icons/unknown_product.jpg', upload_to=shop.models.image_folder, verbose_name='Иконка товара')),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='Описание')),
                ('price', models.FloatField(db_index=True, verbose_name='Цена')),
                ('category', models.ForeignKey(blank=True, default='0000000', on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
                ('user', models.ForeignKey(blank=True, default='0000000', on_delete=django.db.models.deletion.CASCADE, to='users.Profile', verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['name'],
            },
        ),
        migrations.AlterIndexTogether(
            name='category',
            index_together={('id', 'name', 'slug')},
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together={('id', 'name', 'slug')},
        ),
    ]
