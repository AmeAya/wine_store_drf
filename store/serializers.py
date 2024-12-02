from rest_framework.serializers import ModelSerializer
from .models import *


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']
        # fields = '__all__'  # Брать все поля
