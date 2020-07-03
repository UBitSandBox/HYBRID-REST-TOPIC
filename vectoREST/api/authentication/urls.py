from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from api.authentication import views

urlpatterns = [
    path('', views.TokenObtainPairView.as_view()),
    #path('', jwt_views.TokenObtainPairView.as_view()),
    path('refresh/', jwt_views.TokenRefreshView.as_view())
]