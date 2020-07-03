from django.conf.urls import url
from api.config import views

urlpatterns = [
    url('', views.Config.as_view())
]