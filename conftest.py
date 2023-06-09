from types import SimpleNamespace

import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile, BytesIO
from PIL import Image


@pytest.fixture
def authenticated_client():
    user = SimpleNamespace(id=1378, is_authenticated=True)
    _client = APIClient()
    _client.force_authenticate(user=user, token=None)
    return _client


@pytest.fixture
def image_file():
    image = Image.new('RGB', (100, 100), color='white')
    image_bytes = BytesIO()
    image.save(image_bytes, format='jpeg')
    image_bytes.seek(0)

    image_file = SimpleUploadedFile('test_image.png', image_bytes.read(), content_type='image/jpeg')

    yield image_file
