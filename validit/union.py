from validit import Schema
from validit.errors import ValidationUnionError
from validit.utils import shorten, MISSING

from typing import Iterator


class Union(Schema):

    def __init__(self, *options: Schema) -> None:
        self.options = options

    def validate(self, data) -> Iterator[ValidationUnionError]:
        for option in self.options:
            try:
                next(option.validate(data))
            except StopIteration:
                # If there are no errors, this option is valid.
                return

        # If all options are invalid
        yield ValidationUnionError(self.options, data)

    def __repr__(self) -> str:
        extra = ', '.join(repr(op) for op in self.options)
        return f"Union[{shorten(extra)}]"


class Optional(Union):

    def validate(self, data) -> Iterator[ValidationUnionError]:
        if data is MISSING:
            return
        else:
            yield from super().validate(data)

    def __repr__(self) -> str:
        extra = ', '.join(repr(op) for op in self.options)
        return f"Optional[{shorten(extra)}]"
