
from django.conf.urls import url

from .views import BillView


urlpatterns = [
    url(r'^bill/', BillView.as_view()),
]
