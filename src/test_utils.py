from io import BytesIO

from PIL import Image
from botocore.exceptions import ClientError


def create_test_image(width=50, height=50):
    test_image = BytesIO()
    image = Image.new('RGBA', size=(width, height), color=(155, 0, 0))
    image.save(test_image, 'png')
    test_image.name = 'image.png'
    test_image.seek(0)
    return test_image


class BotocoreClientMock:
    def download_fileobj(self, bucket, key, file_obj):
        test_image = create_test_image()
        file_obj.write(test_image.read())

    def upload_fileobj(self, file_obj, bucket, key):
        pass


class BotocoreClientMockError:
    def __init__(self, operation_name):
        self.operation_name = operation_name

    def download_fileobj(self, bucket, key, file_obj):
        raise ClientError(
            error_response={'Error': {'Code': 'Unknown', 'Message': 'Unknown'}}, operation_name=self.operation_name
        )

    def upload_fileobj(self, file_obj, bucket, key):
        raise ClientError(
            error_response={'Error': {'Code': 'Unknown', 'Message': 'Unknown'}}, operation_name=self.operation_name
        )
