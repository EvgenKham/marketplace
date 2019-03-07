from django.contrib import admin
from orders.models import Order, OrderItem

"""Как выводить информацию в admin только с правом просмотра(без права изменения, создания, удаления)???"""


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['customer', 'created']
#
#
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'price', 'quantity']
#
#
# admin.site.register(OrderItem, OrderItemAdmin)
# admin.site.register(Order, OrderAdmin)
