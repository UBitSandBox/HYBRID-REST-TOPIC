from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import VectorSerializer

from ..permissions import VectorsRight


class Vectors(APIView):
    """
    View to obtain dense vector from a doc

    * Requires token authentication.
    * Only member of vector group are able to access this view.
    """
    permission_classes = (IsAuthenticated, VectorsRight)

    def post(self, request):
        """
        Get dense vector from a doc
        :param request:
        :return:
        """

        data = JSONParser().parse(request)
        serializer = VectorSerializer(data=data)

        # TODO: Do something with the data...

        if serializer.is_valid():
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
