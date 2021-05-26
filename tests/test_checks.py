import typing

import pytest
from configTemplate import Template, TemplateList, TemplateDict
from configTemplate.error_managers import TemplateCheckRaiseOnError
from configTemplate.errors import (
    TemplateCheckInvalidDataError as WrongTypeError,
)


class ExampleObj: pass
class SonOfExample(ExampleObj): pass
class AnotherObj: pass


checks = [
    {
        'template': Template(str, int),
        'checks': {
            None: (
                'string', str(), int(), 123456, 0,
            ),
            WrongTypeError: (
                12.34, ExampleObj(), None,
            ),
        },
    },
    {
        'template': TemplateList(Template(str)),
        'checks': {
            None: (
                [],
                tuple(),
                ['hello', 'there!'],
                ('a list', 'of strings!') * 100_100,
            ),
            WrongTypeError: (
                None,
                123,
                set('hello'),
                ['hello', ExampleObj()],
                [None],
            ),
        },
    },
]


params = list()
for test in checks:
    template = test['template']
    for error in test['checks']:
        for data in test['checks'][error]:
            params.append((template, data, error))


@ pytest.mark.parametrize('template, data, error', params)
def test_check_first_error(
        template: Template,
        data: typing.Any,
        error: Exception):

    errors = TemplateCheckRaiseOnError()
    if error is None:
        template.check(data, errors=errors)

    else:
        with pytest.raises(error):
            template.check(data, errors=errors)
