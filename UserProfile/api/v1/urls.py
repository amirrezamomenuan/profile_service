from django.urls import path

from .views import View1


urlpatterns = [
    path('', View1.as_view(), name="test_view"),
]