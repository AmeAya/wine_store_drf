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


# class WineByTypeApiView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request):
#         wine_type = request.GET.get('type')
#         # request.GET.get('ПЕРЕМЕННАЯ') -> Возвращает из ГЕТ параметров переменную ПЕРЕМЕННАЯ.
#         # Если переменной не было, то вернет None
#         wines = Wine.objects.filter(type=wine_type)
#         # .objects.filter(<УСЛОВИЕ>) -> QuerySet всех записей которые подходят по условию <УСЛОВИЕ>
#         data = WineSerializer(instance=wines, many=True).data
#         return Response(data=data, status=status.HTTP_200_OK)


class WineFilterApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        wine_type = request.GET.get('type')
        wine_year = request.GET.get('year')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        wines = Wine.objects.all()
        if wine_type is not None:
            wines = wines.filter(type=wine_type)
        if wine_year is not None:
            wines = wines.filter(year=wine_year)
        if min_price is not None:
            wines = wines.filter(price__gte=min_price)
            # Только те записи у которых price больше или равен чем min_price
        if max_price is not None:
            wines = wines.filter(price__lte=max_price)
            # Только те записи у которых price меньше или равен чем max_price

        # __gt -> Greater Than - Больше чем
        # __lt -> Less Than - Меньше чем
        # __gte -> Greater Than or Equal - Больше или равно
        # __lte -> Greater Than or Equal - Меньше или равно

        data = WineSerializer(instance=wines, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
