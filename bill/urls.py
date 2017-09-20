
from django.conf.urls import url

from .views import BillView


urlpatterns = [
    url(r'^', BillView.as_view()),
]
