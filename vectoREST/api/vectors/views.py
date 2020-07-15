import concurrent

from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import VectorsSerializer
from ..permissions import VectorsRight
from vectoREST.shared import Shared


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
        list_of_supported_lang = ['en', 'fr', 'de', 'it']
        if lang not in list_of_supported_lang:
            raise NotFound(
                detail="Language '{lang}' is not found. Try one of the following : {suggestions}".format(lang=lang,
                                                                                                         suggestions=", ".join(
                                                                                                             list_of_supported_lang)))
        # Get the data from the request
        serializer = VectorsSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        contents = serializer.data
        responses = dict()

        # Get vector in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            results = {executor.submit(Shared.vector_generator.doc2vec, contents[content]): content for content in contents}
            for future in concurrent.futures.as_completed(results):
                result = results[future]
                try:
                    vector = future.result()
                except Exception as exc:
                    #raise ParseError('%r generated an exception: %s' % (result, exc))
                    responses[result] = {"error": exc}
                else:
                    dict_format_response = dict(zip(range(len(vector)), map(float, vector)))
                    response = dict(lang=lang, dense_vector=dict_format_response)
                    print(response)
                    responses[result] = response

        return JsonResponse(responses)
