from unittest import mock

import pytest
from django.urls import reverse
from rest_framework import status

from UserProfile.models import ProfileType, Address, Profile
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


class TestGettingDriverAddress:
    @staticmethod
    def __url():
        return reverse('driver_address_view')

    def test_when_user_is_not_authenticated(self, client):
        response = client.get(self.__url())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_getting_address_when_user_does_not_have_a_profile(
            self,
            authenticated_client
    ):
        response = authenticated_client.get(self.__url())
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_only_address_that_belong_to_user_is_returned(
            self,
            authenticated_client,
            profile_factory,
            address_factory
    ):
        user_profile = profile_factory(user_id=1378, profile_type=ProfileType.Driver)
        address = address_factory(user_profile, 'west-side block1 no2')

        response = authenticated_client.get(self.__url())
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('address') == address.address
        assert response.json().get('city') == address.city.name


class TestEditingDriverAddress:
    @staticmethod
    def __url():
        return reverse('driver_address_view')

    def test_when_user_is_not_authenticated(self, client):
        response = client.put(self.__url())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_editing_address_that_does_not_exist_or_belong_to_driver(
            self,
            authenticated_client,
    ):
        objects_mock = mock.Mock()
        objects_mock.select_related.return_value = objects_mock
        objects_mock.get.side_effect = Address.DoesNotExist()

        with mock.patch('UserProfile.api.v1.views.Address.objects', objects_mock):
            response = authenticated_client.put(self.__url())
            assert response.status_code == status.HTTP_404_NOT_FOUND

    @mock.patch('UserProfile.api.v1.views.AddressSerializer.is_valid')
    def test_if_serializer_is_not_valid(
            self,
            address_serializer_mock,
            authenticated_client,
            address_factory,
            profile_factory,
    ):
        driver_profile = profile_factory(user_id=1378, profile_type=ProfileType.Driver)
        address = address_factory(driver_profile, 'west side, tupac mansion')

        address_serializer_mock.return_value = False
        objects_mock = mock.Mock()
        objects_mock.select_related.return_value = objects_mock
        objects_mock.get.return_value = address

        with mock.patch('UserProfile.api.v1.views.Address.objects', objects_mock):
            response = authenticated_client.put(self.__url())
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    @mock.patch.object(AddressSerializer, 'is_valid')
    @mock.patch.object(AddressSerializer, 'save')
    def test_driver_profile_after_editing_address_successfully(
            self,
            address_serializer_save_mock,
            address_serializer_is_valid_mock,
            authenticated_client,
            profile_factory,
            address_factory
    ):
        driver_profile = profile_factory(user_id=1378, profile_type=ProfileType.Driver)
        address = address_factory(driver_profile, 'west side, tupac mansion')

        objects_mock = mock.Mock()
        objects_mock.select_related.return_value = objects_mock
        objects_mock.get.return_value = address

        address_serializer_is_valid_mock.return_value = True

        with mock.patch('UserProfile.api.v1.views.Address.objects', objects_mock):
            response = authenticated_client.put(self.__url())

            assert response.status_code == status.HTTP_200_OK
            address_serializer_save_mock.assert_called_once()
            assert not driver_profile.is_confirmed


class TestUserProfileView:
    @property
    def __url(self):
        return reverse('user_profile_view')

    @pytest.mark.parametrize(
        'http_method', ['get', 'post', 'put', 'delete']
    )
    def test_unauthorized_request(self, http_method, client):
        assert getattr(client, http_method)(self.__url).status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        'profile_exists, expected_status_code', [
            (True, status.HTTP_200_OK),
            (False, status.HTTP_404_NOT_FOUND)
        ]
    )
    def test_getting_user_profile(
            self,
            profile_exists,
            expected_status_code,
            profile_factory,
            authenticated_client
    ):
        with mock.patch('UserProfile.api.v1.views.Profile.objects.get') as profile_mock:
            if profile_exists:
                profile_mock.return_value = profile_factory(1378, ProfileType.User)
            else:
                profile_mock.side_effect = Profile.DoesNotExist()

            response = authenticated_client.get(self.__url)
            assert response.status_code == expected_status_code

    @mock.patch('UserProfile.api.v1.views.Profile.objects.filter')
    def test_creating_user_profile_when_user_already_has_profile(
            self,
            profile_model_mock,
            authenticated_client
    ):
        profile_objects_mock = mock.Mock()
        profile_objects_mock.exists.return_value = True

        profile_model_mock.return_value = profile_objects_mock
        response = authenticated_client.post(self.__url)
        assert response.status_code == status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

    @pytest.mark.parametrize(
        'is_valid, expected_status_code', [
            (True, status.HTTP_201_CREATED),
            (False, status.HTTP_400_BAD_REQUEST)
        ]
    )
    @mock.patch('UserProfile.api.v1.views.Profile.objects.filter')
    @mock.patch('UserProfile.api.v1.views.ProfileForm')
    def test_creating_user_profile_with_different_form_validation_statuses(
            self,
            profile_form_mock,
            profile_model_mock,
            is_valid,
            expected_status_code,
            authenticated_client
    ):
        profile_objects_mock = mock.Mock()
        profile_objects_mock.exists.return_value = False
        profile_model_mock.return_value = profile_objects_mock

        form_mock = mock.Mock()
        form_mock.is_valid.return_value = is_valid
        form_mock.save.return_value = None
        profile_form_mock.return_value = form_mock

        response = authenticated_client.post(self.__url, data={'some': 'data'})
        assert response.status_code == expected_status_code

        if is_valid:
            form_mock.save.assert_called_once()
        else:
            form_mock.save.assert_not_called()

    def test_updating_user_profile_when_profile_does_not_exist(self):
        assert False

    @pytest.mark.parametrize(
        'is_valid, expected_status_code', [
            (True, status.HTTP_200_OK),
            (False, status.HTTP_400_BAD_REQUEST),
        ]
    )
    def test_updating_user_profile_with_different_form_validation_statuses(
            self,
            is_valid,
            expected_status_code,
            authenticated_client
    ):
        assert False

    def test_deleting_user_profile_successfully(self):
        assert False

    def test_deleting_user_profile_when_it_does_not_exist(self):
        assert False


class TestDriverProfileView:
    @property
    def __url(self):
        return reverse('driver_profile_view')

    @pytest.mark.parametrize(
        'http_method', ['get', 'post', 'put', 'delete']
    )
    def test_unauthorized_request(self, http_method, client):
        assert getattr(client, http_method)(self.__url).status_code == status.HTTP_403_FORBIDDEN

    def test_getting_profile_detail_when_it_does_not_exist(self):
        assert False

    def test_getting_profile_data_is_successful(self):
        assert False

    @pytest.mark.parametrize(
        'is_valid, expected_status_code', [
            (True, status.HTTP_201_CREATED),
            (False, status.HTTP_400_BAD_REQUEST),
        ]
    )
    def test_creating_profile_with_different_form_validations(
            self,
            is_valid,
            expected_status_code,
            authenticated_client
    ):
        assert False

    def test_updating_driver_profile_when_profile_does_not_exist(self):
        assert False

    @pytest.mark.parametrize(
        'is_valid, expected_status_code', [
            (True, status.HTTP_202_ACCEPTED),
            (False, status.HTTP_400_BAD_REQUEST)
        ]
    )
    def test_updating_driver_profile_with_different_form_validations(
            self,
            is_valid,
            expected_status_code,
            authenticated_client
    ):
        assert False

    def test_driver_profile_status_is_changed_to_unavailable_after_modification(self):
        assert False

    def test_deleting_driver_profile_when_it_does_not_exist(self):
        assert False

    def test_deleting_driver_profile_successfully(self):
        assert False

