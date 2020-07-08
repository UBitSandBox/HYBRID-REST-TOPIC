from django.apps import AppConfig
from .VectorGenerator import VectorGenerator


class VectorsConfig(AppConfig):
    name = 'api.vectors'

    vector_generator = VectorGenerator()
