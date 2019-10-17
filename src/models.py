import io

import boto3
from botocore.exceptions import ClientError

from cache import LocalMemoryCache
from config import ACCESS_KEY, SECRET_KEY, S3_BUCKET
from exceptions import ImageUploadException, ImageNotValidException
from validators import ImageValidator


def get_image(image_name):
    """Get image binary from cache if found, else from an S3 bucket

    Raises an ImageDownloadException in case any error occurs while downloading from S3

    :param image_name: Image filename
    :return: ImageModel instance
    """

    cache = LocalMemoryCache()
    image_bytes = cache.get(image_name)
    if not image_bytes:
        s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        try:
            with open(f'/tmp/{image_name}', 'wb+') as image_file:
                s3_client.download_fileobj(S3_BUCKET, image_name, image_file)
                image_file.seek(0)
                image_bytes = image_file.read()
                cache.add(image_name, image_bytes)
        except ClientError:
            return None
    return image_bytes


class Image:
    """Class that represents an ImageModel for handling a class"""

    name = ''
    image_binary = None

    def __init__(self, image_binary, name):
        """Initialize image file and name"""
        self.image_binary = image_binary
        self.name = name

    def cache_image_in_memory(self):
        """Cache image on memory for faster access"""
        cache = LocalMemoryCache()
        cache.add(self.name, self.image_binary)

    def upload_to_server(self, image):
        """Upload image to S3 server

        :return: True if image was uploaded, else False
        """
        s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        try:
            s3_client.upload_fileobj(image, S3_BUCKET, self.name)
        except ClientError:
            return False
        return True

    def save(self):
        """Save image_file to cache and upload to S3

        Raise ImageNotValidException or ImageUploadException if image is invalid or couldn't be uploaded to server

        return: Image uploaded filename
        """
        image = io.BytesIO(self.image_binary)
        validator = ImageValidator()
        if not validator.validate(image):
            raise ImageNotValidException(validator.error)

        self.cache_image_in_memory()

        is_successfully_uploaded = self.upload_to_server(image)
        if not is_successfully_uploaded:
            raise ImageUploadException('Unable to upload image.')
