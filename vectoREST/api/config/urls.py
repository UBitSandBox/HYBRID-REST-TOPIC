from django.conf.urls import url
from api.config import views

urlpatterns = [
    url('', views.getConfig)
]