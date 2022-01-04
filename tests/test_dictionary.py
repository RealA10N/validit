import pytest

from validit import Dictionary, String, Optional
from validit.boolean import Boolean
from validit.errors import ValidationKeyError, ValidationTypeError


class TestDictionary:

    @pytest.mark.parametrize('options, data', (
        (
            {'name': String(r'[a-zA-Z]{3,15}')},
            {'name': 'Alon'}
        ),
        (
            {'name': String(), 'nickname': Optional(String())},
            {'name': 'Alon', 'nickname': 'a10n'}
        ),
        (
            {'name': String(), 'nickname': Optional(String())},
            {'name': 'Alon'}
        ),
        (
            {'name': String(), 'over 18 y/o?': Boolean()},
            {'name': 'Alon', 'over 18 y/o?': True}
        ),
        (
            {'name': String(), 'more': Dictionary(over_18=Boolean())},
            {'name': 'Alon', 'more': {'over_18': True}}
        ),
    ))
    def test_valid(self, options, data):
        errors = tuple(Dictionary(**options).validate(data))
        assert not errors

    @pytest.mark.parametrize('options, data', (
        (
            {'name': String()},
            {'name': 'Alon', 'nickname': 'a10n'}
        ),
    ))
    def test_invalid_key(self, options, data):
        errors = tuple(Dictionary(**options).validate(data))
        assert len(errors) == 1
        assert isinstance(errors[0], ValidationKeyError)

    @pytest.mark.parametrize('options, data', (
        (
            {'name': String()},
            ['hello'],
        ),
        (
            {'name': String()},
            {'name': True},
        ),
        (
            {'name': String()},
            {'name': None},
        ),
        (
            {'name': String()},
            {'name': 123},
        ),
    ))
    def test_invalid_type(self, options, data):
        errors = tuple(Dictionary(**options).validate(data))
        assert len(errors) == 1
        assert isinstance(errors[0], ValidationTypeError)
