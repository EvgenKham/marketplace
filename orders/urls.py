from django.urls import path, re_path
from orders.views import *

app_name = 'orders'

urlpatterns = [
    re_path(r'^buy/$', buy_product, name='buy_product')
]
