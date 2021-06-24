import pytest
import typing

from validit import (
    Template,
    TemplateList,
    TemplateDict,
    TemplateAny,
    Optional,
    Options,
)

from validit.errors.managers import TemplateCheckRaiseOnError
from validit.errors import (
    TemplateCheckInvalidOptionError as InvalidOptionError,
    TemplateCheckInvalidDataError as WrongTypeError,
    TemplateCheckMissingDataError as MissingDataError,
    TemplateCheckListLengthError as ListLengthError,
)

from validit.utils import DefaultValue
from validit.containers import HeadContainer


class ExampleObj: pass
class SonOfExample(ExampleObj): pass
class AnotherObj: pass


checks = [
    {
        'name': 'simple',
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
        'name': 'any',
        'template': TemplateAny(),
        'checks': {
            None: (
                None,
                list(),
                dict(),
                'test',
                123,
                ExampleObj,
                ExampleObj(),
            ),
            MissingDataError: (
                DefaultValue,
            )
        }
    },
    {
        'name': 'list',
        'template': TemplateList(Template(str)),
        'checks': {
            None: (
                [],
                tuple(),
                ['hello', 'there!'],
                ('a list', 'of strings!') * 100,
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
        'name': 'dict',
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
        'name': 'list-of-dicts',
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
    },
    {
        'name': 'list-lengths-set',
        'template': TemplateList(Template(int, float), valid_lengths={1, 2, 3}),
        'checks': {
            None: (
                [21],
                [1, 1.2],
                [1.23, 123, 43],
            ),
            ListLengthError: (
                [],
                [1, 2, 3, 4],
            ),
        },
    },
    {
        'name': 'list-lengths-range',
        'template': TemplateList(Template(int), range(0, 100, 3)),
        'checks': {
            None: (
                [], [1, 1, 1], [0] * 12, [0] * 51, [0] * 99,
            ),
            ListLengthError: (
                [0], [0] * 100, [0] * 31,
            )
        },
    },
    {
        'name': 'optional',
        'template': TemplateDict(
            username=Template(str),
            nickname=Optional(Template(str)),
        ),
        'checks': {
            None: (
                {'username': 'RealA10N', 'nickname': 'Alon'},
                {'username': 'RealA10N'},
            ),
            WrongTypeError: (
                {'username': 'RealA10N', 'nickname': 123},
                {'username': 123},
            ),
            MissingDataError: (
                {'nickname': 'Alon'},
            )
        }
    },
    {
        'name': 'complex-optional',
        'template': TemplateList(TemplateDict(
            username=Template(str),
            realname=Optional(TemplateDict(
                first=Template(str),
                last=Template(str),
            )),
        )),
        'checks': {
            None: (
                list(),
                [{'username': 'Alon'}],
                [
                    {'username': 'Alon'},
                    {'username': 'A10N', 'realname': {
                        'first': 'Alon', 'last': 'Krymgand'}},
                ],
            ),
            MissingDataError: (
                [{'username': 'A10N', 'realname': {'first': 'Alon'}}],
                [{'username': 'A10N', 'realname': {'last': 'Krymgand'}}],
                [
                    {'username': 'Alon'},
                    {'username': 'A10N', 'realname': {'last': 'Krymgand'}}
                ],
                [
                    {'username': 'Alon'},
                    {'username': 'A10N', 'realname': {'last': 'Krymgand'}},
                    {'username': 'A10N', 'realname': {
                        'first': 'Alon', 'last': 'Krymgand'}},
                ],
            ),
            WrongTypeError: (
                None, dict(),
                {'username': 'A10N'},
                [{'username': 123}],
                [{'username': 'A10N', 'realname': {'first': 'Alon', 'last': 123}}],
            )
        }
    },
    {
        'name': 'options-left-right',
        'template': Options('L', 'R'),
        'checks': {
            None: (
                'L', 'R',
            ),
            InvalidOptionError: (
                'r', 'U', 1, None, DefaultValue, ExampleObj, ExampleObj(),
            ),
        },
    },
    {
        'name': 'options-bool-none',
        'template': Options(True, False, None),
        'checks': {
            None: (
                True, False, None,
            ),
            InvalidOptionError: (
                DefaultValue, 'YES', '', 0,
            )
        }
    }
]


def generate_params():
    params = list()
    for test in checks:
        template = test['template']
        name = test['name']
        for error in test['checks']:
            for data in test['checks'][error]:
                params.append(
                    pytest.param(template, data, error, id=name)
                )

    return params


@pytest.mark.parametrize('template, data, error', generate_params())
def test_check_first_error(
        template: Template,
        data: typing.Any,
        error: Exception):

    arguments = {
        'container': HeadContainer(data),
        'errors': TemplateCheckRaiseOnError(),
    }

    if error is None:
        template.validate(**arguments)

    else:
        with pytest.raises(error):
            template.validate(**arguments)
