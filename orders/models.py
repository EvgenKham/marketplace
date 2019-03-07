from django.db import models
from shop.models import Profile
from shop.models import Product


class Order(models.Model):
    customer = models.CharField(max_length=128, verbose_name='Имя заказчика')
    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ: {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

    class Meta:
        ordering = ('order', 'product', 'quantity')
        verbose_name = 'Одна единица заказа'
        verbose_name_plural = 'Несколько единиц заказа'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
