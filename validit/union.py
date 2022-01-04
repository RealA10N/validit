from validit import Schema
from validit.errors import ValidationUnionError
from validit.utils import shorten, MISSING

from typing import Iterator


class Union(Schema):

    def __init__(self, *options: Schema) -> None:
        self.options = options

    def validate(self, data) -> Iterator[ValidationUnionError]:
        for option in self.options:
            if not option.validate(data):
                # If there are no errors, this option is valid.
                return

        # If all options are invalid
        yield ValidationUnionError(self.options, data)

    def __repr__(self) -> str:
        extra = ', '.join(repr(op) for op in self.options)
        return f"Union[{shorten(extra)}]"


class Optional(Union):
    def __init__(self, *options: Schema) -> None:
        super().__init__(MISSING, *options)

    def __repr__(self) -> str:
        extra = ', '.join(repr(op) for op in self.options if op is not MISSING)
        return f"Optional[{shorten(extra)}]"
