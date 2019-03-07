from django.urls import path, re_path
from cart.views import *

app_name = 'cart'

urlpatterns = [
    re_path(r'^remove/(?P<product_id>\d+)/$', cart_remove, name='CartRemove'),
    re_path(r'^add/(?P<product_id>\d+)/$', cart_add, name='CartAdd'),
    path('', cart_detail, name='CartDetail'),
]
