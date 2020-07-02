from django.conf.urls import url
from api.authentication import views

urlpatterns = [
    url('', views.authenticate)
]