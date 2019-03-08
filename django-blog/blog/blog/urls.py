
from django.contrib import admin
from django.urls import path, include
from django_twilio.views import message
from blog import views as blog_views
from blogApp import views
from contact import views as contact_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',blog_views.home_redirect, name='home_redirect'),
    path('admin/', admin.site.urls),
    path('home/', include(('blogApp.urls', 'blogApp')) ),
    path('account/', include('allauth.urls')),
    path('profile/', include(('profiles.urls', 'profiles')) ),
    path('subscribe/', include(('subscribers.urls', 'subscribers'))),
    path('contact/', contact_views.contact, name='contact')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
