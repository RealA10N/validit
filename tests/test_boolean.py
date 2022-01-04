from typing import Any
import pytest

from validit import Boolean
from validit.errors import ValidationTypeError


class TestBoolean:

    @pytest.mark.parametrize('data', (
        True,
        False,
    ))
    def test_valid(self, data: bool):
        errors = tuple(Boolean().validate(data))
        assert not errors

    @pytest.mark.parametrize('data', (
        '',
        'Hello',
        0,
        100,
        None,
        0.0,
        3.14,
    ))
    def test_invalid(self, data):
        errors = tuple(Boolean().validate(data))
        assert len(errors) == 1
        assert isinstance(errors[0], ValidationTypeError)
