import pytest

import math
from fractions import Fraction

from validit import Number, Integer
from validit.errors import ValidationTypeError, ValidationRangeError


class TestNumber:

    @pytest.mark.parametrize('options, data', (
        (
            {},
            (-100**1000, 0, 100**1000, 1, 123, 123.456)
        ),
        (
            {'minimum': 0, 'maximum': 120},
            (0, 120, math.pi, 1, 119, 60, Fraction(1, 2), True, False),
        ),
        (
            {'minimum': 0},
            (0, 0.0, 123456789.987654321, 1, 100, 10**100, 10**1000, 10e-100),
        )
    ))
    def test_valid(self, options, data):
        schema = Number(**options)
        for i in data:
            errors = tuple(schema.validate(i))
            assert not errors

    @pytest.mark.parametrize('options, data', (
        (
            {'minimum': 1},
            (10e-10, 0.000012 + 0.000000000234, -10**100, -1, 0, False),
        ),
        (
            {'maximum': 100},
            (101, 120, 100e100),
        ),
        (
            {'minimum': 0, 'maximum': 120},
            (-1, -10e-10, 121, 100e100),
        ),
    ))
    def test_invalid_range(self, options, data):
        schema = Number(**options)
        for i in data:
            errors = tuple(schema.validate(i))
            assert len(errors) == 1
            assert isinstance(errors[0], ValidationRangeError)

    @pytest.mark.parametrize('data', (
        'string', '123', '123.456', '1.0', None,
    ))
    def test_invalid_type(self, data):
        errors = tuple(Number().validate(data))
        assert len(errors) == 1
        assert isinstance(errors[0], ValidationTypeError)

    @pytest.mark.parametrize('data', (
        -100**1000, 0, 100**1000, 1, 123, 0, 1, 100, 1000, 2**100
    ))
    def test_valid_integer(self, data):
        schema = Integer()
        errors = tuple(schema.validate(data))
        assert not errors

    @pytest.mark.parametrize('data', (
        12.34, 0.0, 1.1, Fraction(1, 2), complex(10, 10)
    ))
    def test_invalid_integer_type(self, data):
        schema = Integer()
        errors = tuple(schema.validate(data))
        assert len(errors) == 1
        assert isinstance(errors[0], ValidationTypeError)
