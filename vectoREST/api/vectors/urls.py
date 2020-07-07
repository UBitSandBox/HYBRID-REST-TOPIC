from django.urls import path
from api.vectors import views

urlpatterns = [
    path('<str:lang>/', views.Vectors.as_view())
]