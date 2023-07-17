from argparse import ArgumentParser
from typing import Type

from extraction import EmailExtractionFromImage, ExtractionFromImage
from validator import ValidateImagePath, ValidateTextPath


class CliInterface:
    def __init__(self, extraction_class: Type[ExtractionFromImage]):
        self.extraction_class = extraction_class
        self.arg_parser = ArgumentParser(
            prog='Extraction email from image',
            description=f'Program extract all {extraction_class.TYPE} from image file.'
        )
        self.arg_parser.add_argument(
            '--input', action=ValidateImagePath,
            type=str, help='the path to the image', required=True
        )
        self.arg_parser.add_argument(
            '--output', action=ValidateTextPath,
            type=str, help='the path to the text file in which the result should be saved'
        )

    def start(self):
        args = self.arg_parser.parse_args()
        extr = self.extraction_class(image_path=args.input, output_path=args.output)
        print(f"List of {self.extraction_class.TYPE} was extracted : {extr.extract()}")
        print(f"Result saved to {extr.save()}")


if __name__ == '__main__':
    cli = CliInterface(EmailExtractionFromImage)
    cli.start()
