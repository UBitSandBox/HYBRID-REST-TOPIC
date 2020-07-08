from django.urls import path, include
from api.config import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'config', views.ConfigViewSet)

urlpatterns = [
    path('', include(router.urls))
]