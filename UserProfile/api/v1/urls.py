from django.urls import path

from .views import (
    UserAddressView,
    DriverAddressView
)


urlpatterns = [
    path('address-list/', UserAddressView.as_view({'get': 'address_list'}), name='user_address_list_view'),
    path('add-address/', UserAddressView.as_view({'post': 'add_address'}), name='user_add_address_view'),
    path(
        'edit-address/<int:address_id>/',
        UserAddressView.as_view({'put': 'edit_address'}),
        name='user_edit_address_view'
    ),
    path(
        'delete-address/<int:address_id>/',
        UserAddressView.as_view({'delete': 'remove_address'}),
        name='user_delete_address_view'
    ),
    path('driver/address/', DriverAddressView.as_view(), name='driver_address_view'),
]
