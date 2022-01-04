import numbers

from validit import Schema
from validit.errors import (
    ValidationError,
    ValidationTypeError,
    ValidationRangeError,
)

from typing import Iterator


class Number(Schema):

    def __init__(
        self,
        minimum: float = None,
        maximum: float = None,
    ) -> None:
        self.minimum = minimum
        self.maximum = maximum

    def validate(self, data) -> Iterator[ValidationError]:
        if not isinstance(data, numbers.Number):
            yield ValidationTypeError(float, data)

        elif self.minimum is not None and data < self.minimum:
            yield ValidationRangeError(data, self.minimum, self.maximum)

        elif self.maximum is not None and data > self.maximum:
            yield ValidationRangeError(data, self.minimum, self.maximum)

    def __repr__(self) -> str:
        mini = f'>={self.minimum}' if self.minimum is not None else ''
        maxi = f'<={self.maximum}' if self.maximum is not None else ''
        extra = ', ' if mini and maxi else ''
        return f'Number[{mini}{extra}{maxi}]'


class Integer(Number):
    def validate(self, data) -> Iterator[ValidationError]:
        if not isinstance(data, int):
            yield ValidationTypeError(int, data)
        else:
            yield from super().validate(data)

    def __repr__(self) -> str:
        mini = f'>={self.minimum}' if self.minimum is not None else ''
        maxi = f'<={self.maximum}' if self.maximum is not None else ''
        extra = ', ' if mini and maxi else ''
        return f'Integer[{mini}{extra}{maxi}]'
