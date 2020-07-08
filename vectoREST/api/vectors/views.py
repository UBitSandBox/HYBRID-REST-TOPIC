import numpy
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .VectorGenerator import VectorGenerator
from .apps import VectorsConfig

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
        dense_vector = VectorsConfig.vector_generator.doc2vec(document=content)



        dict_format_response = dict(zip(range(len(dense_vector)), map(float,dense_vector)))

        print(dict_format_response)

        # dense_vector = {
        #     "0": 0.4433,
        #     "1": 0.2244,
        #     "2": 0.2345
        # }

        response = dict(lang=lang, dense_vector=dict_format_response)
        print(response)

        return JsonResponse(response, safe=True)
