from django.conf.urls import url, include
from rest_framework import routers
from . import views
from django.urls import path

router = routers.DefaultRouter()
router.register(r'contacts', views.ContactViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),

]