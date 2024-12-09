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


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
