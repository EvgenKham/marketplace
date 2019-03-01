from django.urls import path, re_path
from users.views import *

urlpatterns = [
    re_path(r'^register/$', register, name='register'),
    re_path(r'^login/$', login_view, name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^edit/$', edit, name='edit'),
]
