class ImageUploadException(Exception):
    """Exception raised when an Error occurred during upload of image to server"""

    pass


class ImageNotValidException(Exception):
    """Exception raise if image is invalid"""

    def __init__(self, error):
        self.error = error
