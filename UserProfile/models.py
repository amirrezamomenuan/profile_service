from enum import Enum

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError


class ProfileType(Enum):
    User = 1
    Driver = 2


class Car(models.Model):
    plate_number = models.CharField(_('plate number'), max_length=16, unique=True)
    model = models.CharField(_('model'), max_length=64)
    color = models.CharField(_('color'), max_length=16)

    def clean_model(self, value):
        if value not in settings.CAR_MODELS:
            raise ValidationError('model is not valid')
        return value

    def clean_color(self, value):
        if value not in settings.CAR_COLORS:
            raise ValidationError('color is not valid')
        return value

    def clean_fields(self, exclude=None):
        self.clean_model(self.model)
        self.clean_color(self.color)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(args, **kwargs)

    class Meta:
        db_table = 'car'
        verbose_name = 'car'
        verbose_name_plural = 'cars'


class Province(models.Model):
    name = models.CharField(_('province name'), max_length=32)
    latitude = models.FloatField(_('latitude'))
    longitude = models.FloatField(_('longitude'))

    class Meta:
        db_table = 'province'
        verbose_name = 'province'
        verbose_name_plural = 'provinces'


class City(models.Model):
    province = models.ForeignKey(to=Province, on_delete=models.PROTECT, related_name='cities')
    name = models.CharField(_('city name'), max_length=32)
    latitude = models.FloatField(_('latitude'))
    longitude = models.FloatField(_('longitude'))

    class Meta:
        db_table = 'city'
        verbose_name = 'city'
        verbose_name_plural = 'cities'


class Address(models.Model):
    city = models.ForeignKey(to=City, on_delete=models.PROTECT)
    address = models.CharField(_('address'), max_length=255)
    postal_code = models.CharField(_('postal code'), max_length=16, null=True, blank=True)
    owner = models.ForeignKey(to='Profile', on_delete=models.CASCADE, related_name='addresses')

    class Meta:
        db_table = 'address'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'


class DriverProfile(models.Model):
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    user_id = models.PositiveIntegerField(_('user id'), unique=True)
    avatar = models.ImageField(_('driver avatar'))
    phone_number = models.CharField(_('phone number'), max_length=16, unique=True)
    car = models.OneToOneField(to=Car, on_delete=models.PROTECT, related_name='driver')
    address = models.OneToOneField(to=Address, on_delete=models.PROTECT)
    national_id = models.CharField(_('national id'), max_length=16, unique=True)
    is_confirmed = models.BooleanField(_('is confirmed'), default=False)
    register_date = models.DateTimeField(_('register date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        db_table = 'driver_profile'
        verbose_name = 'driver_profile'
        verbose_name_plural = 'driver_profiles'


class Profile(models.Model):
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    user_id = models.PositiveIntegerField(_('user id'), unique=True)
    avatar = models.ImageField(_('driver avatar'), blank=True)
    phone_number = models.CharField(_('phone number'), max_length=16, unique=True)
    national_id = models.CharField(_('national id'), max_length=16, unique=True, null=True)
    register_date = models.DateTimeField(_('register date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'user_profile'
        verbose_name_plural = 'user_profiles'
