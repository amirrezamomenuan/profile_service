import pytest

from UserProfile.models import ProfileType, Profile, Province, City, Address


pytestmark = pytest.mark.django_db


@pytest.fixture
def profile_factory(image_file):
    def _factory(user_id: int, profile_type: ProfileType):
        if profile_type == ProfileType.User:
            _profile = Profile(
                first_name='reza',
                last_name='eivazzadeh',
                user_id=user_id,
                phone_number='09024066963'
            )
            _profile.save()
            return _profile
        else:
            _profile = Profile(
                first_name='reza',
                last_name='eivazzadeh',
                user_id=user_id,
                phone_number='09024066963',
                national_id='0123456789',
                avatar=image_file,
                is_confirmed=True
            )
            _profile.save()
            return _profile

    return _factory


@pytest.fixture
def province():
    return Province.objects.create(
        name='Tehran',
        latitude=35.7219,
        longitude=51.3347
    )


@pytest.fixture
def city(province):
    return City.objects.create(
        name='tehran',
        latitude=35.7219,
        longitude=51.3347,
        province=province
    )


@pytest.fixture
def address_factory(city):
    def _factory(owner, address, postal_code: str = ''):
        return Address.objects.create(
            owner=owner,
            city=city,
            postal_code=postal_code,
            address=address
        )
    return _factory
