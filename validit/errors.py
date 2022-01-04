from typing import Type, Any, Pattern


class ValidationError:
    pass


class ValidationTypeError(ValidationError):

    def __init__(self, expected: Type, got: Any) -> None:
        pass


class ValidationRegexError(ValidationError):
    def __init__(self, string: str, pattern: Pattern) -> None:
        pass
