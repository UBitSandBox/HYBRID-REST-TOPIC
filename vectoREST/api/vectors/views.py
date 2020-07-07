from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError, NotFound
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
            raise NotFound(detail="Language '" + lang + "' is not found")

        # Retrieve the file
        # if 'file' not in request.data:
        #     raise ParseError("A file is required")
        # file = request.data['file']

        if 'content' not in request.data:
            raise ParseError("Content is required")
        content = request.data['content']

        # TODO: Do something with the content...

        dense_vector = {
            "0": 0.4433,
            "1": 0.2244,
            "2": 0.2345
        }

        response = dict(lang=lang, dense_vector=dense_vector)
        return JsonResponse(response, status=status.HTTP_200_OK)
