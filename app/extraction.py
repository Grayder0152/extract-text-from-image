import os
import re
from abc import ABC, abstractmethod
from typing import Optional

import pytesseract

from PIL import Image

from settings import CONFIG_DIR, DEFAULT_IMAGE_LANGUAGE, RESULT_DIR


class ExtractionFromImage(ABC):
    """Abstract class for extraction some text type from the image."""

    TYPE: Optional[str] = None
    PATTERN: Optional[str] = None

    def __init__(self, image_path: str, output_path: Optional[str] = None):
        self.image_path: str = image_path
        self.output_path: Optional[str] = output_path
        self.last_result: Optional[list[str]] = None

    def _parce_by_pattern(self, output: str) -> list:
        """
        Parses text from output by pattern using a regular expression (emails, phone, address ...);

        :param output: str: Pass the output of the command to be parsed;
        :return: A list of matches.
        """

        return re.findall(self.PATTERN, output)

    @abstractmethod
    def extract(self, language: str = DEFAULT_IMAGE_LANGUAGE, tesseract_conf_file: str = CONFIG_DIR) -> list:
        pass

    @abstractmethod
    def save(self) -> str:
        pass


class EmailExtractionFromImage(ExtractionFromImage):
    """Class for extraction email from image and save result to a file."""

    TYPE = 'emails'
    PATTERN = r"[\w.+-]+@[\w-]+\.[\w.-]+"

    def __init__(self, image_path: str, output_path: Optional[str] = None):
        super().__init__(image_path, output_path)

        if self.output_path is None:
            self.output_path = self._generate_output_path()

    def _generate_output_path(self) -> str:
        """
        Generate the path of the output file;
        :return: A string with the path to the output file.
        """

        email_result_path = os.path.join(RESULT_DIR, self.TYPE)
        file_name = f"result_{os.path.basename(self.image_path).split('.')[0]}.txt"
        os.makedirs(email_result_path, exist_ok=True)
        return os.path.join(email_result_path, file_name)

    def extract(self, language: str = DEFAULT_IMAGE_LANGUAGE, tesseract_conf_file: str = CONFIG_DIR) -> list:
        """
        Extract emails from image;
        The function uses the pytesseract library to extract text from the image,
        then parses it using a regex pattern;

        :param language: str: Specify the language of the text in the image;
        :param tesseract_conf_file: str: Specify the path to the tesseract configuration file;
        :return: A list of emails.
        """

        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f'File not found: {self.image_path}')

        img = Image.open(self.image_path)
        output = pytesseract.image_to_string(img, lang=language, config=tesseract_conf_file)
        self.last_result = self._parce_by_pattern(output)
        return self.last_result

    def save(self) -> str:
        """
        The save the extraction last result to a file;
        :return: The output_path, which is a string.
        """

        with open(self.output_path, 'w') as f:
            f.write('\n'.join(self.last_result))
            f.write('\n')
        return self.output_path
