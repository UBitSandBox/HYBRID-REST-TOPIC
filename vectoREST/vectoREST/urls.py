"""vectoREST URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from api.config.models import Config
from vectoREST.VectorGenerator import VectorGenerator
from vectoREST.shared import Shared

# Get configuration for vector generator
currentConfig = Config.objects.latest('id')
Shared.vector_generator = VectorGenerator(method=currentConfig.method, n_clusters=currentConfig.n_clusters)
#for _ in range(3):
#    Shared.vector_generators.append(VectorGenerator(method=currentConfig.method, n_clusters=currentConfig.n_clusters))

baseUrl = "api/v1/"

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routing
    path(baseUrl + "auth/", include('api.authentication.urls')),
    path(baseUrl, include('api.config.urls')),
    path(baseUrl + "vectors/", include('api.vectors.urls'))
]