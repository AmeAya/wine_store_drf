from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Wine(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('Type', on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
    year = models.ForeignKey('Year', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.name) + ' ' + str(self.year.year)


class Winery(models.Model):  # Винодел(Тот кто готовит вино)
    pass


class Year(models.Model):
    year = models.PositiveSmallIntegerField()
    description = models.TextField()

    def __str__(self):
        return str(self.year)
