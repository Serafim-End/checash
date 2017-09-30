# coding: utf-8

from django.conf.urls import url, include
from rest_framework import routers

from .views import ItemViewSet


router = routers.DefaultRouter()

router.register('item', ItemViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
