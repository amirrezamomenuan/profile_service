from enum import Enum

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

from .utils import avatar_upload_path


class ProfileType(Enum):
    User = 1
    Driver = 2


class Car(models.Model):
    plate_number = models.CharField(_('plate number'), max_length=16, unique=True)
    model = models.CharField(_('model'), max_length=64)
    color = models.CharField(_('color'), max_length=16)
    owner = models.OneToOneField(
        verbose_name=_('owner'), to='Profile', null=False, blank=True, on_delete=models.CASCADE
    )

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


class Profile(models.Model):
    profile_type = models.SmallIntegerField(
        _('profile type'),
        choices=[(option.value, option.name) for option in ProfileType],
        default=ProfileType.User.value
    )
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    user_id = models.PositiveIntegerField(_('user id'), unique=True)
    avatar = models.ImageField(_('driver avatar'), upload_to=avatar_upload_path, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=16, unique=True)
    national_id = models.CharField(_('national id'), max_length=16, unique=True, null=True, blank=True)
    is_confirmed = models.BooleanField(_('is confirmed'), default=False)
    register_date = models.DateTimeField(_('register date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)

    class Meta:
        db_table = 'profile'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def clean(self):
        if self.profile_type == ProfileType.Driver:
            if not self.avatar:
                raise ValidationError(_('profile avatar cannot be empty'))
            if not self.national_id:
                raise ValidationError(_('national_id cannot be empty'))

    def save(self, *args, **kwargs):
        if self.profile_type == ProfileType.User:
            self.is_confirmed = True

        self.full_clean()
        super().save(*args, **kwargs)
