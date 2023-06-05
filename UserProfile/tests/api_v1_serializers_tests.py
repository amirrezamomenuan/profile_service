import pytest

from UserProfile.api.v1.serializers import AddressSerializer
from UserProfile.models import ProfileType


pytestmark = pytest.mark.django_db


class TestAddressSerializer:
    @property
    def address_data(self):
        return {
            'address': 'dark side of the moon',
            'postal_code': '12345677890'
        }

    @pytest.mark.parametrize(
        'city_id', [123456, None]
    )
    def test_validation_when_city_with_given_id_does_not_exist(
            self,
            city_id,
            profile_factory
    ):
        data = self.address_data
        if city_id:
            data['city'] = city_id

        user_profile = profile_factory(user_id=1378, profile_type=ProfileType.User)
        serializer = AddressSerializer(data=data, context={'owner_id': user_profile.id})
        assert not serializer.is_valid()

    def test_validation_without_providing_profile_id(
            self,
            city,
    ):
        data = self.address_data
        data['city'] = city.id
        serializer = AddressSerializer(data=data)
        assert not serializer.is_valid()

    def test_validation_and_creation_when_city_exists_with_providing_correct_profile_id(
            self,
            city,
            profile_factory
    ):
        user_profile = profile_factory(user_id=1378, profile_type=ProfileType.User)
        data = self.address_data
        data['city'] = city.id

        serializer = AddressSerializer(data=data, context={'owner_id': user_profile.id})
        assert serializer.is_valid()
        try:
            serializer.save()
        except:
            assert False

    def test_validation_when_profile_with_given_id_does_not_exist(
            self,
            city
    ):
        data = self.address_data
        data['city'] = city.id

        serializer = AddressSerializer(data=data, context={'owner_id': 12345678910})
        assert not serializer.is_valid()

    def test_updating_an_instance_with_different_datas(
            self,
            address_factory,
            profile_factory
    ):
        user_profile = profile_factory(user_id=1378, profile_type=ProfileType.User)
        address = address_factory(user_profile, 'west-side block1 no2')
        serializer = AddressSerializer(instance=address, data=self.address_data, partial=True)

        assert serializer.is_valid()
        try:
            serializer.save()
        except:
            assert False
