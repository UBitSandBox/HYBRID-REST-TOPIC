from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

def getVectors(request):
    if request.method == 'GET':
        return JsonResponse("Get vectors test!", safe=False)
        # 'safe=False' for objects serialization
