import os.path
from abc import ABC, abstractmethod
from argparse import Action, ArgumentParser, Namespace
from typing import Optional

import filetype


class ValidatePath(Action, ABC):
    @abstractmethod
    def validate(self, parser: ArgumentParser, values: str) -> None:
        pass

    def __call__(
            self, parser: ArgumentParser, namespace: Namespace,
            values: str, option_string: Optional[str] = None
    ) -> None:
        self.validate(parser, values)
        setattr(namespace, self.dest, values)


class ValidateTextPath(ValidatePath):
    def validate(self, parser: ArgumentParser, values: str) -> None:
        if not values.endswith('txt'):
            parser.error(f"Please enter a valid text file path (txt file format). Got: {values}")


class ValidateImagePath(ValidatePath):
    def validate(self, parser: ArgumentParser, values: str) -> None:
        if not os.path.exists(values):
            parser.error(f"Image not exists. Got: {values}")
        if not filetype.is_image(values):
            parser.error(f"Please enter a valid image file path. Got: {values}")
