from rest_framework import serializers


class VectorSerializer(serializers.Serializer):
    doc = serializers.CharField()
    lang = serializers.CharField(max_length=2)

    def create(self):
        pass

    def update(self, instance, validated_data):
        pass
