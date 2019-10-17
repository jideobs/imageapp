import re
import imghdr

from utils import get_image_dimensions


class ImageValidator:
    """Class used to validate image files"""

    VALID_MAX_WIDTH = 3000
    VALID_MAX_HEIGHT = 3000

    error = ''

    def validate(self, image_file):
        """Check if image_file is valid

        :param image_file: File pointer to validate
        :return: True if valid, else False
        """

        if image_file is None:
            self.error = "Image file is null"
            return False

        image_file_width, image_file_height = get_image_dimensions(image_file)

        if image_file_width > self.VALID_MAX_WIDTH or image_file_width < 1:
            self.error = f'Make sure image width is between 1 and {self.VALID_MAX_WIDTH}'
            return False

        if image_file_height > self.VALID_MAX_HEIGHT or image_file_width < 1:
            self.error = f'Make sure image height is between 1 and {self.VALID_MAX_HEIGHT}'
            return False

        return True


def is_url_valid(url):
    """Confirm if url passed is valid http URL

    :param url: URL string to validate
    :return: True if valid, else False
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)'
        r'\.(jpeg|jpg|png)$',
        re.IGNORECASE,
    )
    return re.match(regex, url)
