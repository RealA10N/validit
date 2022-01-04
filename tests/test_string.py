import pytest

from validit import String
from validit.errors import ValidationTypeError, ValidationRegexError


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

    @pytest.mark.parametrize('pattern, data', (
        (r'.+', 'Hello There!'),
        (r'\w+', 'OnlyEnglishWorksHere'),
        (r'\w+', 'th1s_sh0uld_BE_FINE_t00'),
        (r'\d+', '1234'),
        (r'\w*', ''),
    ))
    def test_valid_regex(self, pattern: str, data: str):
        errors = tuple(String(pattern).validate(data))
        assert len(errors) == 0

    @pytest.mark.parametrize('pattern, data', (
        (r'.+', str()),
        (r'\w*', 'This is not pure English!'),
        (r'.{,10}', 'This string is too long.'),
    ))
    def test_invalid_regex(self, pattern: str, data: str):
        errors = tuple(String(pattern).validate(data))
        assert len(errors) == 1
        assert isinstance(errors[0], ValidationRegexError)
