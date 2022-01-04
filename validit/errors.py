from validit import Schema

from typing import Type, Any, Pattern, Tuple


class ValidationError:
    pass


class ValidationTypeError(ValidationError):

    def __init__(self, expected: Type, got: Any) -> None:
        pass


class ValidationRegexError(ValidationError):
    def __init__(self, string: str, pattern: Pattern) -> None:
        pass


class ValidationUnionError(ValidationError):
    def __init__(self, expected: Tuple[Schema], got: Any) -> None:
        pass


class ValidationKeyError(ValidationError):
    def __init__(self, key: str) -> None:
        pass


class ValidationRangeError(ValidationError):
    def __init__(self,
                 got: float,
                 minimun: float = None,
                 maximum: float = None,
                 ) -> None:
        pass
