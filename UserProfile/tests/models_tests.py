from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from django.conf import settings

from UserProfile.models import Car

pytestmark = pytest.mark.django_db


class TestCarModel:
    @mock.patch.object(Car, 'clean_model')
    def test_creating_car_when_given_model_is_not_valid_should_fail(self, car_mock):
        car_mock.side_effect = ValidationError('')
        car = Car(
            plate_number='12ab4234',
            color=settings.CAR_COLORS.pop(),
            model='some bad model name'
        )
        try:
            car.save()
            assert False
        except ValidationError:
            assert True

    @mock.patch.object(Car, 'clean_color')
    def test_creating_car_with_invalid_color_should_fail(self, car_mock):
        car_mock.side_effect = ValidationError('')
        car = Car(
            plate_number='12ab4234',
            color='some really bad color',
            model=settings.CAR_MODELS.pop()
        )
        try:
            car.save()
            assert False
        except ValidationError:
            assert True

    @mock.patch.object(Car, 'clean_color')
    @mock.patch.object(Car, 'clean_model')
    def test_creating_car_with_unique_plate_number_and_valid_color_and_model_should_pass(
            self,
            model_mock,
            color_mock,
    ):
        try:
            Car(
                plate_number='12ab4234',
                color=settings.CAR_COLORS.pop(),
                model=settings.CAR_MODELS.pop()
            ).save()
        except ValidationError:
            assert False
