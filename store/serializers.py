from rest_framework.serializers import ModelSerializer
from .models import *


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']
        # fields = '__all__'  # Брать все поля


class WineSerializer(ModelSerializer):
    class Meta:
        model = Wine
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country'] = instance.country.name
        representation['type'] = instance.type.name
        return representation


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'age', 'number']
