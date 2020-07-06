from django.urls import path
from api.vectors import views

urlpatterns = [
    path('', views.Vectors.as_view())
]