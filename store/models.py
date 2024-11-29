from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)


class Type(models.Model):
    name = models.CharField(max_length=255)


class Wine(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)

    type = models.ForeignKey('Type', on_delete=models.PROTECT)
    price = models.PositiveIntegerField()


class Winery(models.Model):  # Винодел(Тот кто готовит вино)
    pass


class Year(models.Model):
    year = models.PositiveSmallIntegerField()
    description =  models.TextField()
