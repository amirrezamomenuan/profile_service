from types import SimpleNamespace

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def authenticated_client():
    user = SimpleNamespace(id=1378, is_authenticated=True)
    _client = APIClient()
    _client.force_authenticate(user=user, token=None)
    return _client
