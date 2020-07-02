from django.shortcuts import render
from .apps import Doc2VecConfig
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class call_model(APIView):

    def get(self,request):
        if request.method == 'GET':
            
            content =  request.GET.get('body')
            lang = request.GET.get('lang')
            method = request.GET.get('method') or "k-means"
        
            lang_switcher = {
                'en': Doc2VecConfig.en_nlp,
                'it': Doc2VecConfig.it_nlp,
                'fr': Doc2VecConfig.fr_nlp,
                'de': Doc2VecConfig.de_nlp,

            }
            
            doc = lang_switcher[lang](content)
            preprocessed_words = [token.lemma_.lower() for token in doc if not any([token.is_stop,token.is_punct,token.is_digit,token.is_currency])]
            response = Doc2VecConfig.aggregate([Doc2VecConfig.vectorise(word,lang) for word in preprocessed_words], method)
            
            header = {
                "lang" : lang,
                "method" : method,
                "pre-processed text" : " ".join(preprocessed_words)
            }

            dict_format_response = {**header, **dict(zip(range(len(response)), response))}
            return JsonResponse(dict_format_response, safe=True)