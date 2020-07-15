from rest_framework import serializers


class VectorsSerializer(serializers.Serializer):
    _0 = serializers.CharField(required=True)
    _1 = serializers.CharField(required=False)
    _2 = serializers.CharField(required=False)
    _3 = serializers.CharField(required=False)
    _4 = serializers.CharField(required=False)
