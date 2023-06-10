from rest_framework import serializers

from UserProfile.models import Address, City, Profile


class AddressListSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ['city', 'address', 'postal_code']

    def get_city(self, instance):
        return instance.city.name


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all()
    )
    owner = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all()
    )

    class Meta:
        model = Address
        fields = ['city', 'address', 'postal_code', 'owner']

    def to_internal_value(self, data):
        if 'owner_id' in self.context:
            owner_id = self.context.get('owner_id')
            data['owner'] = owner_id
        return super().to_internal_value(data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']
