from dataclasses import dataclass

from validit import Schema
from validit.errors import ValidationError


from typing import Any, Tuple, Union, Type


@dataclass
class ValidationResults:
    schema: Schema
    data: Any
    errors: Tuple[ValidationError]


def validate(schema: Union[Type, Schema], data) -> ValidationResults:
    errors = tuple(schema.validate(data))
    return ValidationResults(schema, data, errors)
