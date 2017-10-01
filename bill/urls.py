
from django.conf.urls import url

from .views import BillView, BillFPView


urlpatterns = [
    url(r'^bill/', BillView.as_view()),
    url(r'^bill/fp/', BillFPView.as_view())
]
