from django.conf.urls import url
from api.vectors import views

urlpatterns = [
    url('', views.getVectors)
]