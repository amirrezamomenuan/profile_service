from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from UserProfile.models import Address, Profile
from .serializers import AddressListSerializer, AddressSerializer


class UserAddressView(ViewSet):
    permission_classes = [IsAuthenticated, ]

    def address_list(self, request):
        # TODO: add_caching
        addresses = Address.objects.select_related(
            'city',
        ).filter(
            owner__user_id=request.user.id
        )
        addresses_data = AddressListSerializer(addresses, many=True).data

        return Response(data={'addresses': addresses_data})

    def add_address(self, request):
        try:
            user_profile = Profile.objects.get(
                user_id=request.user.id
            )
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('you dont have a profile yet')}
            )

        address_serializer_data = AddressSerializer(
            data=request.data,
            context={'owner_id': user_profile.id}
        )

        if address_serializer_data.is_valid():
            address_serializer_data.save()
            # TODO: add cache deletion
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': _('added address')}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': _('invalid data')}
        )

    def edit_address(self, request, address_id):
        try:
            address = Address.objects.get(
                id=address_id,
                owner__user_id=request.user.id
            )
        except Address.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': _('address that you want to modify is not found')}
            )

        address_serializer = AddressSerializer(data=request.data, instance=address)

        if address_serializer.is_valid():
            address_serializer.save()
            return Response(
                status=status.HTTP_200_OK,
                data={'message': _('address edited')}
            )
            # TODO: add cache deletion
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': _('invalid data')}
        )

    def remove_address(self, request, address_id):
        try:
            Address.objects.get(
                id=address_id,
                owner__user_id=request.user.id
            ).delete()
            # TODO: add cache deletion
        except Address.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': _('address that you want to delete does not')}
            )
        else:
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
