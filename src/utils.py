import requests
from PIL import Image
from requests import RequestException


def get_image_dimensions(image_file_path):
    """Get image dimensions from file

    :param image_file_path: Location of image
    :return: Image's size
    """
    with Image.open(image_file_path) as img:
        return img.size


def download_image_from_url(url):
    """Download image from URL

    :param url: Image URL to fetch image from
    :return: None if an error while fetching, else return content byte
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except RequestException:
        return None
    return response.content
