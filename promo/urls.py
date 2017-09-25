# coding: utf-8

from django.conf.urls import url, include
from rest_framework import routers

from .views import PromoViewSet, PublicPromos


router = routers.DefaultRouter()

router.register('promo', PromoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^public/', PublicPromos.as_view()),
]
