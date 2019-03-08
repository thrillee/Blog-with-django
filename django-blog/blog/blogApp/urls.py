from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'create/$', create_post, name='create_post'),
    re_path(r'update/(?P<post>[-\w]+)/$', post_update, name='post_update'),
    re_path(r'delete/(?P<post>[-\w]+)/$', delete_post, name='delete_post'),
    re_path(r'details/(?P<post>[-\w]+)/$', post_details, name='post_details'),
    re_path(r'(?P<category>[-\w]+)/$', post_list, name='post_list'),



    ]
