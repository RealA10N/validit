import typing

import pytest
from configTemplate import Template, TemplateList, TemplateDict
from configTemplate.error_managers import TemplateCheckRaiseOnError
from configTemplate.errors import (
    TemplateCheckInvalidDataError as WrongTypeError,
    TemplateCheckMissingDataError as MissingDataError,
    TemplateCheckListLengthError as ListLengthError,
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
    {
        'template': TemplateDict(
            username=Template(str),
            code=Template(int),
        ),
        'checks': {
            None: (
                {'username': 'RealA10N', 'code': 123},
                {'username': '', 'code': 0, ExampleObj: AnotherObj()},
            ),
            WrongTypeError: (
                {'username': 'RealA10N', 'code': '123'},
                {'code': 123, 'username': str},
            ),
            MissingDataError: (
                dict(),
                {'code': 123},
            )
        }
    },
    {
        'template': TemplateList(TemplateDict(
            username=Template(str),
            code=Template(int),
        )),
        'checks': {
            None: (
                list(),
                [
                    {'username': 'RealA10N', 'code': 123},
                    {'username': 'elonmusk', 'code': 42069},
                ],
            ),
            WrongTypeError: (
                {'username': 'RealA10N', 'code': 123},
                [ExampleObj()],
                [
                    {'username': 'RealA10N', 'code': 123},
                    {'username': 'elonmusk', 'code': 12.34},
                ],
            ),
            MissingDataError: (
                [{'username': 'RealA10N'}],
                [
                    {'username': 'RealA10N', 'code': 123},
                    {'code': 456},
                ],
            )
        }
    }
]


def generate_params():
    params = list()
    for test in checks:
        template = test['template']
        for error in test['checks']:
            for data in test['checks'][error]:
                params.append((template, data, error))
    return params


@pytest.mark.parametrize('template, data, error', generate_params())
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
