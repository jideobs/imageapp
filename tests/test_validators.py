from unittest import TestCase

from test_utils import create_test_image
from validators import ImageValidator


class ImageValidatorTests(TestCase):
    def setUp(self):
        self.validator = ImageValidator()

    def test_validate__image_file_null(self):
        self.assertFalse(self.validator.validate(None))
        self.assertEqual('Image file is null', self.validator.error)

    def test_validate__image_file__invalid_width(self):
        test_image = create_test_image(3000, 3000)
        self.assertFalse(self.validator.validate(test_image))
        self.assertEqual(
            f'Make sure image width is between 1 and {ImageValidator.VALID_MAX_WIDTH}', self.validator.error
        )

    def test_validate__image_file__invalid_height(self):
        test_image = create_test_image(1280, 3000)
        self.assertFalse(self.validator.validate(test_image))
        self.assertEqual(
            f'Make sure image height is between 1 and {ImageValidator.VALID_MAX_HEIGHT}', self.validator.error
        )

    def test_validate__valid_image(self):
        test_image = create_test_image(1280, 800)
        self.assertTrue(self.validator.validate(test_image))
        self.assertEqual('', self.validator.error)
