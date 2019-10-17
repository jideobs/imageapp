import pytest

from web import IMAGE_APP


@pytest.fixture(scope='class', autouse=True)
def client(request):
    IMAGE_APP.config['TESTING'] = True
    request.cls.client = IMAGE_APP.test_client()
