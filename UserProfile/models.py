from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError


class Car(models.Model):
    plate_number = models.CharField(verbose_name=_('plate number'), max_length=16, unique=True)
    model = models.CharField(verbose_name=_('model'), max_length=64)
    color = models.CharField(verbose_name=_('color'), max_length=16)


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
