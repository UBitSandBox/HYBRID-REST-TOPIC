from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..permissions import VectorsRight


class Vectors(APIView):
    """
    View to obtain dense vector from a doc

    * Requires token authentication.
    * Only member of vector group are able to access this view.
    """

    # Set policy right
    permission_classes = (IsAuthenticated, VectorsRight)

    def post(self, request, lang):
        """
        Get dense vector from a doc
        :param lang:
        :param request:
        :return:
        """

        # Check if lang is correct
        if lang != 'en' and \
           lang != 'fr' and \
           lang != 'de' and \
           lang != 'it':
            return JsonResponse("error", status=status.HTTP_422_UNPROCESSABLE_ENTITY, safe=False)
        # TODO: Create a class error for this


        # Retrieve the file
        if 'file' not in request.data:
            raise ParseError("File is required")
        file = request.data['file']

        # TODO: Do something with the file...

        # TODO: Return a reel response
        return JsonResponse("ok!", status=status.HTTP_200_OK, safe=False)
