import os
from unittest import TestCase, main

from app.extraction import EmailExtractionFromImage
from app.settings import BASE_DIR

TEST_EMAILS_IMG_PATH = os.path.join(BASE_DIR, 'tests', 'images', 'emails')
RESULT_PATH = 'result.txt'


class EmailExtractionFromImageTestCase(TestCase):
    def test_init(self):
        self.assertTrue(hasattr(EmailExtractionFromImage, 'TYPE'))
        self.assertTrue(hasattr(EmailExtractionFromImage, 'PATTERN'))
        self.assertEqual(EmailExtractionFromImage.TYPE, 'emails')
        self.assertIsNotNone(EmailExtractionFromImage.PATTERN)

        image_path, output_path = 'image.jpg', 'result.txt'
        extr = EmailExtractionFromImage(image_path, output_path)
        self.assertTrue(hasattr(extr, 'image_path'))
        self.assertTrue(hasattr(extr, 'output_path'))
        self.assertTrue(hasattr(extr, 'last_result'))
        self.assertEqual(extr.image_path, image_path)
        self.assertEqual(extr.output_path, output_path)
        self.assertIsNone(extr.last_result)

        extr = EmailExtractionFromImage(image_path)
        self.assertTrue(hasattr(extr, 'output_path'))
        self.assertTrue(extr.output_path.endswith(f"result_{os.path.basename(image_path).split('.')[0]}.txt"))

    def test_extract(self):
        with self.assertRaises(FileNotFoundError):
            EmailExtractionFromImage('not_exists_image.jpg').extract()

        image_path = os.path.join(TEST_EMAILS_IMG_PATH, 'test_1.jpg')
        extr = EmailExtractionFromImage(image_path)

        result = extr.extract()
        self.assertIsInstance(result, list)
        self.assertEqual(result, extr.last_result)
        self.assertEqual(result[0], 'ralphie.buffalo@colorado.edu')

        extr.image_path = os.path.join(TEST_EMAILS_IMG_PATH, 'test_2.png')
        result = extr.extract()
        self.assertEqual(result[0], 'tiara.parisian@gmail.com')

        extr.image_path = os.path.join(TEST_EMAILS_IMG_PATH, 'test_3.png')
        result = extr.extract()
        self.assertIn('peter_wilson@businessmail.com', result)

    def test_save(self):
        image_path, result_path = os.path.join(TEST_EMAILS_IMG_PATH, 'test_1.jpg'), RESULT_PATH
        extr = EmailExtractionFromImage(image_path, result_path)
        result = extr.extract()

        self.assertFalse(os.path.exists(RESULT_PATH))
        extr.save()
        self.assertTrue(os.path.exists(RESULT_PATH))
        with open(RESULT_PATH) as f:
            data = f.read().replace('\n', '')
        self.assertEqual(data, result[0])

    def tearDown(self) -> None:
        if os.path.exists(RESULT_PATH):
            os.remove(RESULT_PATH)


if __name__ == '__main__':
    main()
