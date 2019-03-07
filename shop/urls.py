from django.urls import path, re_path
from shop.views import *

urlpatterns = [
    path('', index, name='index'),
    re_path(r'^category/(?P<slug>[-\w]+)/$', view_category, name='category_detail'),
    re_path(r'^product/(?P<slug>[-\w]+)/$', view_product, name='product_detail'),
    re_path(r'^add_product/$', add_product, name='add_product'),
    ]
