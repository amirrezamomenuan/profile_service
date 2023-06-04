from rest_framework import serializers

from UserProfile.models import Address, City


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

    class Meta:
        model = Address
        fields = ['city', 'address', 'postal_code', 'owner']
