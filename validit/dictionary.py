from typing import Iterator
from validit import Schema
from validit.errors import ValidationError, ValidationTypeError, ValidationKeyError

from validit.utils import MISSING, shorten


class Dictionary(Schema):
    def __init__(self, **options: Schema) -> None:
        self.options = options

    def validate(self, data) -> Iterator[ValidationError]:
        if not isinstance(data, dict):
            yield ValidationTypeError(dict, data)
            return

        for key in data:
            if key not in self.options:
                yield ValidationKeyError(key)

        for key, schema in self.options.items():
            yield from schema.validate(data.get(key, MISSING))

    def __repr__(self) -> str:
        extra = ', '.join((
            f"{key!r}={schema!r}"
            for key, schema in self.options.items()
        ))
        return f'Dictionary[{shorten(extra)}]'
