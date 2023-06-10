from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from UserProfile.models import Address, Profile, ProfileType
from .serializers import AddressListSerializer, AddressSerializer, ProfileSerializer
from .forms import ProfileForm


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

        address_serializer = AddressSerializer(instance=address, data=request.data, partial=True)

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


class DriverAddressView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            address = Address.objects.get(
                owner__user_id=request.user.id,
            )
        except Address.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': _('address not found')}
            )
        address_data = AddressListSerializer(address, many=False).data

        return Response(data=address_data)

    def put(self, request):
        try:
            address = Address.objects.select_related(
                'owner'
            ).get(
                owner__user_id=request.user.id,
            )
        except Address.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': _('address not found')}
            )

        address_serializer = AddressSerializer(instance=address, data=request.data, partial=True)

        if address_serializer.is_valid():
            with transaction.atomic():
                address_serializer.save()
                address.owner.is_confirmed = False
                address.owner.save()
            # TODO: add cache deletion
            return Response(
                status=status.HTTP_200_OK,
                data={'message': _('address edited, waiting for confirmation')}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'message': _('invalid data')}
        )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            user_profile = Profile.objects.get(
                user_id=request.user.id,
                profile_type=ProfileType.User.value
            )
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': _('profile not found')}
            )

        profile_data = ProfileSerializer(user_profile, many=False).data
        return Response(data=profile_data)

    def post(self, request):
        profile_form = ProfileForm(data=request.GET)

        if profile_form.is_valid():
            profile_form.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': _('profile created successfully')}
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('invalid data')}
            )

    def put(self, request):
        try:
            user_profile = Profile.objects.get(
                user_id=request.user.id,
                profile_type=ProfileType.User.value
            )
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('profile not found')}
            )

        profile_form = ProfileForm(data=request.GET, instance=user_profile, partial=True)

        if profile_form.is_valid():
            profile_form.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': _('profile created successfully')}
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('invalid data')}
            )

    def delete(self, request):
        try:
            Profile.objects.get(
                user_id=request.user.id,
                profile_type=ProfileType.User.value
            ).delete()
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('profile not found')}
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={'message': _('profile deleted successfully')}
        )


class DriverProfileView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        try:
            driver_profile = Profile.objects.get(
                user_id=request.user.id,
                profile_type=ProfileType.User.value
            )
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'message': _('profile not found')}
            )

        profile_data = ProfileSerializer(driver_profile, many=False).data
        return Response(data=profile_data)

    def post(self, request):
        profile_form = ProfileForm(data=request.GET)

        if profile_form.is_valid():
            profile_form.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': _('profile created successfully')}
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('invalid data')}
            )

    def put(self, request):
        try:
            driver_profile = Profile.objects.get(
                user_id=request.user.id,
                profile_type=ProfileType.Driver.value
            )
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('profile not found')}
            )

        profile_form = ProfileForm(data=request.GET, instance=driver_profile, partial=True)

        if profile_form.is_valid():
            profile_form.save()
            return Response(
                status=status.HTTP_201_CREATED,
                data={'message': _('profile created successfully')}
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('invalid data')}
            )

    def delete(self, request):
        try:
            Profile.objects.get(
                user_id=request.user.id,
                profile_type=ProfileType.Driver.value
            ).delete()
        except Profile.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'message': _('profile not found')}
            )

        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={'message': _('profile deleted successfully')}
        )
