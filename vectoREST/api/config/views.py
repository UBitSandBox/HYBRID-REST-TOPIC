from django.shortcuts import render

from django.http.response import JsonResponse
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Config
from .serializers import ConfigSerializer

from ..permissions import ConfigRight


class ConfigList(APIView):
    """
    View to list all configurations in the system.

    * Requires token authentication.
    * Only member of config group are able to access this view.
    """

    # Set API policy
    permission_classes = (IsAuthenticated, ConfigRight)

    def get(self, request):
        """
        Return a list of all configurations
        :param request:
        :return:
        """
        configs = Config.objects.all()
        serializer = ConfigSerializer(configs, many=True)
        return JsonResponse(serializer.data, safe=False)
        # 'safe=False' for objects serialization

    def post(self, request):
        """
        Create a new configuration
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        serializer = ConfigSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfigDetail(APIView):
    """
    View to list a specific configurations in the system.

    * Requires token authentication.
    * Only member of config group are able to access this view.
    """

    def get_object(self, pk):
        try:
            return Config.objects.get(pk=pk)
        except Config.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        config = self.get_object(pk)
        serializer = ConfigSerializer(config)
        return Response(serializer.data)
