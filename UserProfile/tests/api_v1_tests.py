from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status

from UserProfile.models import ProfileType, Address
from UserProfile.api.v1.serializers import AddressSerializer

pytestmark = pytest.mark.django_db


class TestGettingUserAddresses:
    @staticmethod
    def __url():
        return reverse('user_address_list_view')

    def test_when_user_is_not_authenticated(self, client):
        response = client.get(self.__url())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_getting_addresses_when_user_does_not_have_a_profile_or_address(
            self,
            authenticated_client
    ):
        response = authenticated_client.get(self.__url())
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('addresses') == []

    def test_only_addresses_that_belong_to_user_are_returned(
            self,
            authenticated_client,
            profile_factory,
            address_factory
    ):
        user_profile = profile_factory(user_id=1378, profile_type=ProfileType.User)
        address = address_factory(user_profile, 'west-side block1 no2')

        response = authenticated_client.get(self.__url())
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json().get('addresses')) == user_profile.addresses.count()
        assert response.json().get('addresses')[0].get('address') == address.address
        assert response.json().get('addresses')[0].get('city') == address.city.name


class TestAddingNewAddressForUser:
    @staticmethod
    def __url():
        return reverse('user_add_address_view')

    def test_when_user_is_not_authenticated(self, client):
        response = client.post(self.__url())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_adding_address_when_user_does_not_have_profile(
            self,
            authenticated_client
    ):
        with mock.patch('UserProfile.api.v1.views.AddressSerializer') as address_serializer_mock:
            response = authenticated_client.post(self.__url())
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            address_serializer_mock.assert_not_called()

    @pytest.mark.parametrize(
        'serializer_should_validate, expected_status_code', [
            (True, status.HTTP_201_CREATED),
            (False, status.HTTP_400_BAD_REQUEST)
        ]
    )
    @mock.patch.object(AddressSerializer, 'is_valid')
    @mock.patch.object(AddressSerializer, 'save')
    @mock.patch('UserProfile.api.v1.views.Profile.objects.get')
    def test_adding_address_with_different_serializer_validations(
            self,
            profile_mock,
            address_serializer_save,
            address_serializer_is_valid,
            serializer_should_validate,
            expected_status_code,
            authenticated_client
    ):
        user_profile = mock.Mock()
        user_profile.id = 123
        profile_mock.return_value = user_profile

        address_serializer_is_valid.return_value = serializer_should_validate
        response = authenticated_client.post(self.__url(), data={'some': 'data'})

        assert response.status_code == expected_status_code
        if serializer_should_validate:
            address_serializer_save.assert_called_once()
        else:
            address_serializer_save.assert_not_called()


class TestEditingAddress:

    @staticmethod
    def __url(address_id):
        return reverse('user_edit_address_view', kwargs={'address_id': address_id})

    def test_when_user_is_not_authenticated(self, client):
        response = client.put(self.__url(address_id=1))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @mock.patch('UserProfile.api.v1.views.Address.objects.get')
    def test_editing_address_when_address_with_given_id_does_not_exist(
            self,
            address_mock,
            authenticated_client
    ):
        address_mock.side_effect = Address.DoesNotExist

        response = authenticated_client.put(self.__url(address_id=1))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        'serializer_should_validate, expected_status_code', [
            (True, status.HTTP_200_OK),
            (False, status.HTTP_400_BAD_REQUEST)
        ]
    )
    @mock.patch.object(AddressSerializer, 'is_valid')
    @mock.patch.object(AddressSerializer, 'save')
    @mock.patch('UserProfile.api.v1.views.Address.objects.get')
    def test_editing_address_with_different_serializer_validations(
            self,
            address_mock,
            address_serializer_save,
            address_serializer_is_valid,
            serializer_should_validate,
            expected_status_code,
            authenticated_client,
            address_factory,
            profile_factory
    ):
        user_profile = profile_factory(user_id=1378, profile_type=ProfileType.User)
        address = address_factory(user_profile, 'west-side block1 no2')

        address_mock.return_value = address
        address_serializer_is_valid.return_value = serializer_should_validate

        response = authenticated_client.put(self.__url(address_id=address.id), data={'some': 'data'})

        assert response.status_code == expected_status_code
        if serializer_should_validate:
            address_serializer_save.assert_called_once()
        else:
            address_serializer_save.assert_not_called()


class TestDeletingUserAddress:
    @staticmethod
    def __url(address_id):
        return reverse('user_delete_address_view', kwargs={'address_id': address_id})

    def test_when_user_is_not_authenticated(self, client):
        response = client.delete(self.__url(address_id=1))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @mock.patch('UserProfile.api.v1.views.Address.objects.get')
    def test_deleting_when_address_with_given_id_does_not_exist_or_belong_to_user(
            self,
            address_mock,
            authenticated_client
    ):
        address_mock.side_effect = Address.DoesNotExist
        response = authenticated_client.delete(self.__url(address_id=123))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deleting_address_successfully(
            self,
            address_factory,
            profile_factory,
            authenticated_client
    ):
        user_profile = profile_factory(user_id=1378, profile_type=ProfileType.User)
        address = address_factory(user_profile, 'west-side block1 no2')
        response = authenticated_client.delete(self.__url(address_id=address.id))
        assert response.status_code == status.HTTP_204_NO_CONTENT
