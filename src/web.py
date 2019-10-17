import io
import mimetypes
from flask import Flask, request, json, Response, send_file, url_for

from exceptions import ImageUploadException, ImageNotValidException
from utils import download_image_from_url
from validators import is_url_valid
from models import Image, get_image

IMAGE_APP = Flask(__name__)


def build_response(message, code, data=None):
    """Util to build JSON response

    :param message: Information detailing status of request
    :param code: HTTP Status code of request
    :param data: Optional data to send with request
    :return: Flask Response object
    """

    if data is None:
        data = {}

    response_body = {'message': message, 'data': data, 'code': code}
    response_json = json.dumps(response_body)

    return Response(response_json, status=code, mimetype='application/json')


@IMAGE_APP.route('/')
def index():
    """Index page."""

    return '<h1>Image app</h1>'


@IMAGE_APP.route('/image/view/<image_name>')
def view(image_name):
    """Get image if found."""

    image_bytes = get_image(image_name)
    if image_bytes is None:
        return '<h1>Image Not Found</h1>'

    return send_file(
        io.BytesIO(image_bytes),
        attachment_filename=image_name,
        mimetype=mimetypes.guess_type(image_name, strict=True)[0],
    )


@IMAGE_APP.route('/image/upload', methods=['POST'])
def upload():
    """Upload image from passed URL."""

    # Validate is image URL.
    request_data = request.get_json()
    if request_data is None or request_data.get('image_url', None) is None:
        return build_response('Request data invalid or Image URL not found.', 400)

    image_url = request_data.get('image_url')
    if not is_url_valid(image_url):
        return build_response('Image URL not valid.', 400)

    # Download image from URL.
    image_bytes = download_image_from_url(image_url)
    if image_bytes is None:
        return build_response('Unable to download image from URL, try again.', 400)

    # Upload image to servers and add to cache.
    try:
        image_name = image_url[image_url.rfind('/') + 1 :]
        image = Image(image_bytes, image_name)
        image.save()
    except ImageNotValidException as e:
        return build_response(f'Image validation error: {e.error}', 400)
    except ImageUploadException:
        return build_response('Unable to upload image to server', 500)

    # Return new image URL
    image_url = url_for(endpoint='view', image_name=image_name, _external=True)
    return build_response('Image uploaded successfully', 201, data={'image_url': image_url})


if __name__ == '__main__':
    IMAGE_APP.run()
