from django.urls import path, re_path
from users.views import *

app_name = 'users'

urlpatterns = [
    re_path(r'^register/$', register_view, name='register'),
    re_path(r'^login/$', login_view, name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^edit/$', edit_view, name='edit'),
    re_path(r'^account/$', account_view, name='account'),
]
