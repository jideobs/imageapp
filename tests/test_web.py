import json
from unittest import TestCase

import pytest
import responses
from mock import patch

from test_utils import BotocoreClientMock, BotocoreClientMockError, create_test_image


@pytest.mark.usefixtures("client")
class IndexTests(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(200, response.status_code)

        self.assertEqual(b'<h1>Image app</h1>', response.data)


@pytest.mark.usefixtures("client")
class ViewTests(TestCase):
    def test_view_image__not_found(self):
        with patch('models.boto3.client') as MockClient:
            MockClient.return_value = BotocoreClientMockError('download_fileobj')
            response = self.client.get('/image/view/unknownimage.png')

        self.assertEqual(b'<h1>Image Not Found</h1>', response.data)

    def test_view_image__image_found(self):
        with patch('models.boto3.client') as MockClient:
            MockClient.return_value = BotocoreClientMock()
            response = self.client.get('/image/view/image.png')
            self.assertEqual(200, response.status_code)
            self.assertIsNotNone(response.data)


@pytest.mark.usefixtures("client")
class UploadTests(TestCase):
    def test_upload__invalid_image_url(self):
        response = self.client.post(
            '/image/upload',
            data=json.dumps({'image_url': 'http://www.google.com/file.txt'}),
            content_type='application/json',
        )
        self.assertEqual(400, response.status_code)

        expected_response_data = {'message': 'Image URL not valid.', 'data': {}, 'code': 400}
        self.assertEqual(expected_response_data, json.loads(response.data))

    def test_upload__invalid_request_data(self):
        response = self.client.post('/image/upload', data=json.dumps({}), content_type='application/json')
        self.assertEqual(400, response.status_code)

        expected_response_data = {'message': 'Request data invalid or Image URL not found.', 'data': {}, 'code': 400}
        self.assertEqual(expected_response_data, json.loads(response.data))

    @responses.activate
    def test_upload__unable_to_download_image(self):
        responses.add(responses.GET, 'http://www.google.com/image.png', body=None, status=404)

        response = self.client.post(
            '/image/upload',
            data=json.dumps({'image_url': 'http://www.google.com/image.png'}),
            content_type='application/json',
        )
        self.assertEqual(400, response.status_code)

        expected_response_data = {'message': 'Unable to download image from URL, try again.', 'data': {}, 'code': 400}
        self.assertEqual(expected_response_data, json.loads(response.data))

    @responses.activate
    def test_upload__image_not_valid(self):
        test_image = create_test_image(width=30000)
        responses.add(responses.GET, 'http://www.google.com/image.png', body=test_image.read(), status=200)

        response = self.client.post(
            '/image/upload',
            data=json.dumps({'image_url': 'http://www.google.com/image.png'}),
            content_type='application/json',
        )
        self.assertEqual(400, response.status_code)

        expected_response_data = {
            'message': 'Image validation error: Make sure image width is between 1 and 3000',
            'data': {},
            'code': 400,
        }
        self.assertEqual(expected_response_data, json.loads(response.data))

    @responses.activate
    def test_upload__image_upload_error(self):
        test_image = create_test_image()
        responses.add(responses.GET, 'http://www.google.com/image.png', body=test_image.read(), status=200)

        with patch('models.boto3.client') as MockClient:
            MockClient.return_value = BotocoreClientMockError('upload_fileobj')

            response = self.client.post(
                '/image/upload',
                data=json.dumps({'image_url': 'http://www.google.com/image.png'}),
                content_type='application/json',
            )
            self.assertEqual(500, response.status_code)

            expected_response_data = {'message': 'Unable to upload image to server', 'data': {}, 'code': 500}
            self.assertEqual(expected_response_data, json.loads(response.data))

    @responses.activate
    def test_upload__success(self):
        test_image = create_test_image()
        responses.add(responses.GET, 'http://www.google.com/image.png', body=test_image.read(), status=200)

        response = self.client.post(
            '/image/upload',
            data=json.dumps({'image_url': 'http://www.google.com/image.png'}),
            content_type='application/json',
        )
        self.assertEqual(201, response.status_code)

        expected_response_data = {
            'message': 'Image uploaded successfully',
            'data': {'image_url': 'http://localhost/image/view/image.png'},
            'code': 201,
        }
        self.assertEqual(expected_response_data, json.loads(response.data))
