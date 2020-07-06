from django.urls import path
from api.config import views

urlpatterns = [
    path('', views.ConfigList.as_view()),
    path('<int:pk>/', views.ConfigDetail.as_view())
]