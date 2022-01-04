from .schema import Schema
from .errors import ValidationError, ValidationRegexError, ValidationTypeError

from typing import Iterator, Pattern


class String(Schema):

    def __init__(self, pattern: Pattern = None) -> None:
        self.pattern = pattern

    def validate(self, data) -> Iterator[ValidationError]:
        if not isinstance(data, str):
            yield ValidationTypeError(str, data)
        elif self.pattern is not None:
            if not self.pattern.fullmatch(data):
                yield ValidationRegexError(data, self.pattern)

    def __repr__(self) -> str:
        extra = str()
        if self.pattern is not None:
            extra = f'[{self.pattern.pattern}]'
        return 'String' + extra
