import concurrent

from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated

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

        serializer = VectorsSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors)

        contents = serializer.data

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = [executor.submit(Shared.vector_generator.doc2vec, contents[id_content]) for id_content in
                       contents]

            for f in concurrent.futures.as_completed(results):
                vector = f.result()
                dict_format_response = dict(zip(range(len(vector)), map(float, vector)))
                response = dict(lang=lang, dense_vector=dict_format_response)

        return JsonResponse(response.data)



        # if 'content' not in request.data:
        #     raise ParseError("Content is required")
        #
        # content = request.data['content']
        # dense_vector = Shared.vector_generator.doc2vec(document=content)
        # dict_format_response = dict(zip(range(len(dense_vector)), map(float, dense_vector)))
        # response = dict(lang=lang, dense_vector=dict_format_response)
        #
        # # Test
        # with concurrent.futures.ProcessPoolExecutor() as executor:
        #     results = [executor.submit(Shared.vector_generator.doc2vec, content) for i in range(10)]
        #
        #     for f in concurrent.futures.as_completed(results):
        #         print(f.result())
        #
        # return JsonResponse(response, safe=True)
