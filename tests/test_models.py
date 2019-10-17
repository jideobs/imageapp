from unittest import TestCase

from mock import patch

from cache import LocalMemoryCache
from exceptions import ImageNotValidException, ImageUploadException
from models import get_image, Image
from test_utils import create_test_image, BotocoreClientMock, BotocoreClientMockError


class GetImageTests(TestCase):
    def setUp(self):
        self.image_name = 'image.png'

    def test_get_image__cache(self):
        test_image = create_test_image()
        cache = LocalMemoryCache()
        cache.add('image.png', test_image)
        image_binary = get_image(self.image_name)

        self.assertEqual(test_image, image_binary)

        cache.delete(self.image_name)  # Clean up

    def test_get_image__s3(self):
        with patch('models.boto3.client') as MockClient:
            MockClient.return_value = BotocoreClientMock()
            image_binary = get_image(self.image_name)
            self.assertIsNotNone(image_binary)

    def test_get_image__client_error(self):
        with patch('models.boto3.client') as MockClient:
            MockClient.return_value = BotocoreClientMockError('download_fileobj')
            image_binary = get_image(self.image_name)
            self.assertIsNone(image_binary)


class ImageTests(TestCase):
    def test_save__invalid_image(self):
        test_image = create_test_image(4000, 4000)

        with self.assertRaises(ImageNotValidException):
            image = Image(test_image.read(), 'image.png')
            image.save()

    def test_save__unable_to_upload_to_server(self):
        test_image = create_test_image()
        with patch('models.boto3.client') as MockClient:
            MockClient.return_value = BotocoreClientMockError('upload_fileobj')

            with self.assertRaises(ImageUploadException):
                image = Image(test_image.read(), 'image.png')
                image.save()

    def test_save__save_successful(self):
        test_image = create_test_image()
        with patch('models.boto3.client') as MockClient:
            MockClient.return_value = BotocoreClientMock()

            # Just check if it runs.
            image = Image(test_image.read(), 'image.png')
            image.save()
