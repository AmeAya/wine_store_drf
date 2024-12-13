from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


class CountryApiView(APIView):
    permission_classes = [IsAuthenticated]  # AllowAny -> Доступна АПИ всем

    def get(self, request):  # Что делать на GET запрос
        countries = Country.objects.all()  # QuerySet со всеми записями из модели Country
        data = CountrySerializer(instance=countries, many=True).data
        # instance -> Параметр сериалайзера, который принимает объект для конвертации в JSON
        # many -> True, если в instance несколько объектов(> 1)
        # .data -> Вытаскиваем данные в виде JSON
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):  # POST запрос служит для создания новый записей
        country = CountrySerializer(data=request.data)  # Даем JSON, получаем Джанго объект
        # request.data -> Body, тело запроса, в котором передаются данные
        if country.is_valid():  # is_valid() - проверяет все ли данные в request.data подходям полям модельки
            country.save()  # save() - сохраняем объект в базу данных
            return Response(data={'message': 'OK!'}, status=status.HTTP_200_OK)
        return Response(data=country.errors, status=status.HTTP_400_BAD_REQUEST)
        # .errors - Показывает ошибки сериалайзера

    def patch(self, request):  # PATCH запрос служит для изменения уже существующих записей
        country_id = request.data.get('id')
        if country_id is None:
            return Response(data={'message': 'Field "id" is required!'}, status=status.HTTP_400_BAD_REQUEST)

        from django.shortcuts import get_object_or_404
        country = get_object_or_404(Country, id=country_id)
        # get_object_or_404(<МОДЕЛЬ>, <УСЛОВИЕ>) - Возвращает объект - одну запись, которая подходит по <УСЛОВИЕ>
        #                                          из модели <МОДЕЛЬ>
        # Если найдено меньше 1 записи, то возвращает ответ, что запись не найдена с кодом 404
        # Если найдено больше 1 записи, то вызывает ошибку MultipleObjectsReturned

        updated_country = CountrySerializer(instance=country, data=request.data, partial=True)
        # partial -> Если стоит False, то тогда сериалайзер будет требовать все поля
        # partial -> Если стоит True, то сериалайзер обновляет только те поля, которые есть в request.data

        if updated_country.is_valid():
            updated_country.save()  # Сохранить запись с обновлениями
            return Response(data={'message': 'OK!'}, status=status.HTTP_200_OK)
        return Response(data=updated_country.errors, status=status.HTTP_400_BAD_REQUEST)

        # .objects.get(<УСЛОВИЕ>) -> Возвращает объект - одну запись, которая подходит по <УСЛОВИЕ>
        # country = Country.objects.get(id=-100)
        # Если найдено меньше 1 записи, то вызывает ошибку DoesNotExist
        # country = Country.objects.get(name='Spain')
        # Если найдено больше 1 записи, то вызывает ошибку MultipleObjectsReturned

    def delete(self, request):
        country_id = request.data.get('id')
        if country_id is None:
            return Response(data={'message': 'Field "id" is required!'}, status=status.HTTP_400_BAD_REQUEST)
        from django.shortcuts import get_object_or_404
        country = get_object_or_404(Country, id=country_id)
        country.delete()  # .delete() -> Метод моделек, который удаляет запись из БД
        return Response(data={'message': 'OK!'}, status=status.HTTP_200_OK)


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


class AuthApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):  # Авторизация делается POST запросом, а не GET
        from django.contrib.auth import authenticate, login

        email = request.data.get('email')
        if email is None:
            return Response(data={'message': 'Field "email" is required!'}, status=status.HTTP_400_BAD_REQUEST)
        password = request.data.get('password')
        if password is None:
            return Response(data={'message': 'Field "password" is required!'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        # authenticate -> Хэширует пароль и с имейлом идет проверять, есть ли такой юзер
        # Если имейл и пароль совпали, то вернет юзера. Иначе, то вернет None
        if user is None:
            return Response(data={'message': 'Email and/or Password is not valid!'}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        # login -> Генерирует ключи доступа, записывает в БД какие ключи принадлежат этому юзеру.
        # А также, возвращает их обратно юзеру

        return Response(data={'message': 'Welcome'}, status=status.HTTP_200_OK)


class RegistrationApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email is None:
            return Response(data={'message': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if password is None:
            return Response(data={'message': 'Password is required!'}, status=status.HTTP_400_BAD_REQUEST)

        password1 = request.data.get('password1')
        if password1 is None:
            return Response(data={'message': 'Password1 is required!'}, status=status.HTTP_400_BAD_REQUEST)

        if password != password1:
            return Response(data={'message': 'Password and Password1 not match!'}, status=status.HTTP_400_BAD_REQUEST)

        CustomUser.objects.create_user(email=email, password=password)
        return Response(data={'message': 'User Created!'}, status=status.HTTP_200_OK)


class UserCabinetApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user -> Юзер, который отправил запрос на эту АПИ.
        data = CustomUserSerializer(instance=request.user, many=False).data
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = CustomUserSerializer(instance=request.user, data=request.data, partial=True)
        if user.is_valid():
            user.save()
            return Response(data=user.data, status=status.HTTP_200_OK)
        return Response(data=user.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response(data={'message': 'Delete!'}, status=status.HTTP_200_OK)


class MealApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        import requests  # pip install requests
        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
        meal = response.json()
        data = {
            'name': meal['meals'][0]['strMeal'],
            'recipe': meal['meals'][0]['strInstructions']
        }
        return Response(data=data, status=status.HTTP_200_OK)


class WineSearchApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        name = request.GET.get('name')
        if name is None:
            wines = Wine.objects.all()
        else:
            wines = Wine.objects.filter(name__icontains=name)
            # contains -> Чувствителен к регистру.
            # icontains -> Не чувствителен к регистру.

        data = WineSerializer(instance=wines, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)


from rest_framework.pagination import PageNumberPagination
class WinePaginatedApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        all_wines = Wine.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 2
        wines = paginator.paginate_queryset(all_wines, request)
        data = WineSerializer(instance=wines, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)
