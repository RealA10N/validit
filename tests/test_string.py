from abc import abstractclassmethod
import pytest

from validit import String
from validit.errors import ValidationTypeError


class TestString:

    @pytest.mark.parametrize('data', (
        str(),
        'hello!',
        'שלום לכם!',
        '123',
    ))
    def test_valid_no_regex(self, data):
        errors = tuple(String().validate(data))
        assert len(errors) == 0

    @pytest.mark.parametrize('data', (
        None,
        123,
        12.34,
        0,
        True,
        False,
    ))
    def test_invalid_no_regex(self, data):
        errors = tuple(String().validate(data))
        assert len(errors) == 1
        assert isinstance(errors[0], ValidationTypeError)
