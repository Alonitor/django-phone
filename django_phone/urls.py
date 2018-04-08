"""django_phone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf import settings

# ##### DAVY ####
# from davvy.base import WebDAV
# from davvy.addressbook import CardDAV
# from davvy.calendar import CalDAV
# ##############

#######  DJRadicale ################
from djradicale.views import DjRadicaleView, WellKnownView
#######  END DJRadicale ############

if settings.RECAPTCHA_ADMIN:
    from captcha_admin import admin
else:
    from django.contrib import admin

urlpatterns = [    
    #url(r'^', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^contacts/', include('contacts.urls')),
    url(r'^api/', include('api.urls')),

    # ##### DAVY ####
    # # url(r'^principals/(\w+)/(.*)', WebDAV.as_view(root='storage')),
    # # url(r'^storage/(\w+)/(.*)', WebDAV.as_view(root='storage')),
    # # url(r'^addressbook/(\w+)/(.*)', CardDAV.as_view(root='addressbook001')),
    # # url(r'^calendars/(\w+)/(.*)', CalDAV.as_view(root='calendars')),
    #
    # # url(r'^.well[-_]?known/caldav/?$', WellKnownDAV.as_view(root='calendars')),
    # url(r'^.well[-_]?known/carddav/?$', WellKnownDAV.as_view(root='addressbook001')),
    # ##############

    #######  DJRadicale ################

    url(r'^' + settings.DJRADICALE_CONFIG_EXTRA['server']['base_prefix'].lstrip('/'),
        include(('djradicale.urls', 'djradicale'))),

    # .well-known external implementation
    url(r'^\.well-known/(?P<type>(caldav|carddav))$',
        WellKnownView.as_view(), name='djradicale_well-known'),

    #######  END DJRadicale ############
]
