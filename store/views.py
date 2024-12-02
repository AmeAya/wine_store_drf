from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


class CountryApiView(APIView):
    permission_classes = [AllowAny]  # AllowAny -> Доступна АПИ всем

    def get(self, request):  # Что делать на GET запрос
        countries = Country.objects.all()  # QuerySet со всеми записями из модели Country
        data = CountrySerializer(instance=countries, many=True).data
        # instance -> Параметр сериалайзера, который принимает объект для конвертации в JSON
        # many -> True, если в instance несколько объектов(> 1)
        # .data -> Вытаскиваем данные в виде JSON
        return Response(data=data, status=status.HTTP_200_OK)

# TypeApiView -> GET функцию, которая возвращает все из модели Type
# TypeSerializer
