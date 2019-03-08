from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'(?P<username>[-\w]+)/$', user_profile, name='user_profile'),
]
