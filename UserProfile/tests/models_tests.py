import pytest

pytestmark = pytest.mark.django_db


class TestCarModel:
    def test_creating_car_with_duplicate_plate_numbers_should_fail(self):
        assert True

    def test_creating_car_when_given_model_is_not_valid_should_fail(self):
        assert True

    def test_creating_car_with_invalid_color_should_fail(self):
        assert True

    def test_creating_car_with_unique_plate_number_and_valid_color_and_model_should_pass(self):
        assert True