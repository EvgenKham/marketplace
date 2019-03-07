from django.db import models
from django.urls import reverse
from users.models import Profile
from django.template.defaultfilters import slugify


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format("icon_save_products", filename)


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Категория', db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, blank=True)
    pass

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'name', 'slug']
        ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, default="0000000")
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Владелец', blank=True, default="0000000")
    name = models.CharField(max_length=100, verbose_name='Название', db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, blank=True)
    icon = models.ImageField(upload_to=image_folder, verbose_name="Иконка товара", blank=True,
                             default="icons/unknown_product.jpg")
    description = models.TextField(verbose_name='Описание', max_length=500, blank=True)
    price = models.FloatField(verbose_name='Цена', db_index=True)

    class Meta:
        ordering = ['name']
        index_together = [
            'id', 'name', 'slug'
        ]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return str(self.name)
        pass

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


