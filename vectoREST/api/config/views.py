from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class Config(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse("Get config test!", safe=False)
        # 'safe=False' for objects serialization
