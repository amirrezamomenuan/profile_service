import pytest
from rest_framework import status


class TestGettingUserAddresses:
    def test_getting_addresses_when_user_is_not_authenticated(self):
        assert True

    def test_getting_addresses_when_user_does_not_have_a_profile(self):
        assert True

    def test_only_addresses_that_belong_to_user_are_returned(self):
        assert True


class TestGettingDriverAddress:
    def test_getting_addresses_when_user_is_not_authenticated(self):
        assert True

    def test_getting_address_when_user_does_not_have_a_profile(self):
        assert True

    def test_only_address_that_belong_to_user_is_returned(self):
        assert True


class TestAddingNewAddressForUser:
    def test_adding_address_when_user_is_not_authenticated(self):
        assert True

    def test_adding_address_when_user_does_not_have_profile(self):
        assert True

    def test_adding_address_with_different_datas(self):
        assert True

    def test_adding_address_for_user_profile_with_correct_data(self):
        assert True


class TestAddingNewAddressForDriver:
    def test_adding_address_when_user_is_not_authenticated(self):
        assert True

    def test_adding_address_when_user_does_not_have_profile(self):
        assert True

    def test_adding_address_with_different_datas(self):
        assert True

    @pytest.mark.parametrize(
        'already_has_address, expected_status', [
            (True, status.HTTP_400_BAD_REQUEST),
            (False, status.HTTP_201_CREATED),
        ]
    )
    def test_adding_address_for_driver_profile_with_correct_data(
            self,
            already_has_address,
            expected_status
    ):
        assert True

    def test_adding_address_for_user_profile_with_correct_data(self):
        assert True


class TestEditingAddress:
    def test_editing_address_when_user_is_not_authenticated(self):
        assert True

    def test_editing_address_when_address_with_given_id_does_not_exist(self):
        assert True

    def test_editing_address_when_address_with_given_id_does_not_belong_to_user(self):
        assert True

    def test_editing_address_with_different_datas(self):
        assert True


class TestEditingDriverAddress:
    def test_editing_driver_address_when_user_is_not_authenticated(self):
        assert True

    def test_editing_driver_address_when_driver_does_not_have_a_profile(self):
        assert True

    def test_editing_address_that_does_not_exist_or_belong_to_driver(self):
        assert True

    def test_successful_address_editing(self):
        assert True


class TestDeletingUserAddress:
    def test_deleting_address_when_user_is_not_authenticated(self):
        assert True

    def test_deleting_address_when_user_does_not_have_profile(self):
        assert True

    def test_deleting_when_address_with_given_id_does_not_exist_or_belong_to_user(self):
        assert True
