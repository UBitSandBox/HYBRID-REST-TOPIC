from rest_framework import serializers
from .models import Config

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ['id',
                  'method',
                  'n_clusters',
                  'min_length',
                  'max_length',
                  'vector_dimension',
                  'description',
                  'created_at']

