from django.urls import path
from api.config import views

urlpatterns = [
    path('', views.ConfigView.as_view()),
    path('history/', views.ConfigList.as_view()),
    path('history/<int:pk>/', views.ConfigDetail.as_view())
]