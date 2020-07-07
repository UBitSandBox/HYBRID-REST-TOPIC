from rest_framework import serializers
from .models import Config, METHOD

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

# class ConfigSerializer(serializers.Serializer):
#
#     id = serializers.IntegerField(read_only=True)
#     method = serializers.CharField(required=True, allow_blank=False, choices=METHOD)
#     n_clusters = serializers.IntegerField()
#     min_length = serializers.IntegerField()
#     max_length = serializers.IntegerField()
#
#     def create(self, validated_data):
#         """
#         Create and return and new `Config` instance, given the validated data.
#         :param validated_data:
#         :return:
#         """
#
#         return Config.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         pass
