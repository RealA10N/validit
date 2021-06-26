import pytest
import typing
from dataclasses import dataclass

from validit import (
    Template,
    TemplateList,
    TemplateDict,
    TemplateAny,
    Optional,
    Options,
)

from validit.templates import BaseTemplate

from validit.errors.managers import TemplateCheckRaiseOnError
from validit.errors import (
    TemplateCheckError,
    TemplateCheckInvalidOptionError as InvalidOptionError,
    TemplateCheckInvalidDataError as WrongTypeError,
    TemplateCheckMissingDataError as MissingDataError,
    TemplateCheckListLengthError as ListLengthError,
)

from validit.utils import DefaultValue
from validit.containers import HeadContainer


class ExampleObj: ...  # noqa: E701
class AnotherObj: ...  # noqa: E701


@dataclass(frozen=True)
class Check:
    data: typing.Any
    error: typing.Type[TemplateCheckError] = None
    msg: typing.Optional[str] = None


@dataclass(frozen=True)
class CheckGroup:
    cases: typing.List[typing.Any]
    error: typing.Type[TemplateCheckError] = None

    def to_checks(self,):
        return [Check(data, self.error) for data in self.cases]


@dataclass(frozen=True)
class SingleTest:
    template: BaseTemplate
    check: Check

    def run(self,):
        arguments = {
            'container': HeadContainer(self.check.data),
            'errors': TemplateCheckRaiseOnError(),
        }

        if self.check.error is None:
            self.template.validate(**arguments)

        else:
            with pytest.raises(self.check.error):
                self.template.validate(**arguments)


@dataclass(frozen=True)
class TemplateTest:
    name: str
    template: BaseTemplate
    checks: typing.List[typing.Union[Check, CheckGroup]]

    def collect_checks(self,):
        final = list()
        for check in self.checks:
            if isinstance(check, CheckGroup):
                final.extend(check.to_checks())
            else:
                final.append(check)
        return final

    def to_single_tests(self,):
        return [
            SingleTest(template=self.template, check=check)
            for check in self.collect_checks()
        ]


@dataclass(frozen=True)
class CollectionTest:
    tests: typing.List[TemplateTest]

    def to_single_tests(self,):
        return [
            single
            for test in self.tests
            for single in test.to_single_tests()
        ]


tests = CollectionTest([
    TemplateTest(
        name='simple',
        template=Template(str, int),
        checks=[
            CheckGroup([
                'string', str(), int(), 123456, 0,
            ]),
            Check(
                ExampleObj(),
                error=WrongTypeError,
                msg="Expected 'str' or 'int' but got 'ExampleObj'",
            ),
            Check(
                DefaultValue,
                error=MissingDataError,
                msg='Missing required information',
            ),
        ]
    ),
    TemplateTest(
        name='any',
        template=TemplateAny(),
        checks=[
            CheckGroup([
                None,
                list(),
                dict(),
                'test',
                123,
                ExampleObj,
                ExampleObj(),
            ]),
            Check(DefaultValue, MissingDataError),
        ]
    ),
    TemplateTest(
        name='list',
        template=TemplateList(Template(str)),
        checks=[
            CheckGroup([
                [],
                tuple(),
                ['hello', 'there!'],
                ('a list', 'of strings!') * 100,
            ]),
            Check(
                123,
                error=WrongTypeError,
                msg="Expected 'list' or 'tuple' but got 'int'",
            ),
            CheckGroup([
                None,
                set('hello'),
                ['hello', ExampleObj()],
                [None],
            ], error=WrongTypeError)
        ]
    ),
    TemplateTest(
        name='dict',
        template=TemplateDict(
            username=Template(str),
            code=Template(int)
        ),
        checks=[
            CheckGroup([
                {'username': 'RealA10N', 'code': 123},
                {'username': '', 'code': 0, ExampleObj: AnotherObj()},
            ]),
            CheckGroup([
                {'username': 'RealA10N', 'code': '123'},
                {'code': 123, 'username': str},
            ], error=WrongTypeError),
            CheckGroup([
                dict(),
                {'code': 123},
            ], error=MissingDataError),
        ],
    ),
    TemplateTest(
        name='list-of-dicts',
        template=TemplateList(TemplateDict(
            username=Template(str),
            code=Template(int),
        )),
        checks=[
            CheckGroup([
                list(),
                [
                    {'username': 'RealA10N', 'code': 123},
                    {'username': 'elonmusk', 'code': 42069},
                ],
            ]),
            CheckGroup([
                {'username': 'RealA10N', 'code': 123},
                [ExampleObj()],
                [
                    {'username': 'RealA10N', 'code': 123},
                    {'username': 'elonmusk', 'code': 12.34},
                ],
            ], error=WrongTypeError),
            CheckGroup([
                [{'username': 'RealA10N'}],
                [
                    {'username': 'RealA10N', 'code': 123},
                    {'code': 456},
                ],
            ], error=MissingDataError),
        ],
    ),
    TemplateTest(
        name='list-length-set',
        template=TemplateList(Template(int, float), valid_lengths={1, 2, 3}),
        checks=[
            CheckGroup([
                [21],
                [1, 1.2],
                [1.23, 123, 43],
            ]),
            CheckGroup([
                [],
                [1, 2, 3, 4],
            ], error=ListLengthError),
            CheckGroup([
                [1, 'notnum'],
                'notlist',
            ], error=WrongTypeError),
        ],
    ),
    TemplateTest(
        name='list-lengths-range',
        template=TemplateList(Template(int), range(0, 100, 3)),
        checks=[
            CheckGroup([
                [],
                [1, 1, 1],
                [0] * 12,
                [0] * 51,
                [0] * 99,
            ]),
            CheckGroup([
                [0],
                [0] * 100,
                [0] * 31,
            ], error=ListLengthError),
        ],
    ),
    TemplateTest(
        name='optional',
        template=TemplateDict(
            username=Template(str),
            nickname=Optional(Template(str)),
        ),
        checks=[
            CheckGroup([
                {'username': 'RealA10N', 'nickname': 'Alon'},
                {'username': 'RealA10N'},
            ]),
            CheckGroup([
                {'username': 'RealA10N', 'nickname': 123},
                {'username': 123},
            ], error=WrongTypeError),
            CheckGroup([
                {'nickname': 'Alon'},
            ], error=MissingDataError),
        ],
    ),
    TemplateTest(
        name='complex-optional',
        template=TemplateList(TemplateDict(
            username=Template(str),
            realname=Optional(TemplateDict(
                first=Template(str),
                last=Template(str),
            )),
        )),
        checks=[
            CheckGroup([
                list(),
                [{'username': 'Alon'}],
                [
                    {'username': 'Alon'},
                    {'username': 'A10N', 'realname': {
                        'first': 'Alon', 'last': 'Krymgand'}},
                ],
            ]),
            CheckGroup([
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
            ], error=MissingDataError),
            CheckGroup([
                None, dict(),
                {'username': 'A10N'},
                [{'username': 123}],
                [{'username': 'A10N', 'realname': {'first': 'Alon', 'last': 123}}],
            ], error=WrongTypeError),
        ]
    ),
    TemplateTest(
        name='options-left-right',
        template=Options('L', 'R'),
        checks=[
            CheckGroup(['L', 'R']),
            CheckGroup([
                'r',
                'U',
                None,
                DefaultValue,
                ExampleObj,
                ExampleObj(),
            ], error=InvalidOptionError),
            Check(
                21,
                error=InvalidOptionError,
                msg="Expected 'L' or 'R' but got 21"
            ),
        ]
    ),
    TemplateTest(
        name='optional-options',
        template=Optional(Options('jpeg', 'png', 'gif'), default='gif'),
        checks=[
            CheckGroup(['jpeg', 'png', 'gif']),
            Check(DefaultValue),
            CheckGroup(['hello', 123, None], error=InvalidOptionError)
        ],
    ),
])


@pytest.mark.parametrize('test', tests.to_single_tests())
def test_check_first_error(test: SingleTest):

    arguments = {
        'container': HeadContainer(test.check.data),
        'errors': TemplateCheckRaiseOnError(),
    }

    if test.check.error is None:
        test.template.validate(**arguments)

    else:
        with pytest.raises(test.check.error) as einfo:
            test.template.validate(**arguments)

        error: TemplateCheckError = einfo.value
        if test.check.msg is not None and error.msg != test.check.msg:
            pytest.fail(
                '\n'.join([
                    'Expected message:',
                    test.check.msg,
                    'But instead got message:',
                    error.msg,
                ])
            )
