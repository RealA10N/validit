from typing import Iterator
from validit import Schema
from validit.errors import ValidationTypeError


class Boolean(Schema):

    def validate(self, data) -> Iterator[ValidationTypeError]:
        if not isinstance(data, bool):
            yield ValidationTypeError(bool, data)

    def __repr__(self) -> str:
        return 'Boolean'
