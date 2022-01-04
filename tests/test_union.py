import pytest


from validit import Union, Boolean, String
from validit.errors import ValidationUnionError

import re


class TestUnion:

    @pytest.mark.parametrize('options, data', (
        ((Boolean(), String()), 'this is a string'),
        ((Boolean(), String()), True),
        ((Boolean(), String()), False),
        ((Boolean(),), False),
        ((Boolean(),), True),
        ((String(),), 'Hello'),
    ))
    def test_valid(self, options, data):
        errors = tuple(Union(*options).validate(data))
        assert not errors

    @pytest.mark.parametrize('options, data', (
        ((Boolean(), String(re.compile('.+'))), ''),
        ((Boolean(), String()), None),
        (tuple(), None)
    ))
    def test_invalid(self, options, data):
        errors = tuple(Union(*options).validate(data))
        assert len(errors) == 1
        assert isinstance(errors[0], ValidationUnionError)
