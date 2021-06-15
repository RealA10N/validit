import pytest

from validit.utils import DefaultValue
from validit.containers import HeadContainer

from validit import (
    Template,
    TemplateDict,
    TemplateList,
    Optional,
)

cases = [
    {
        'name': 'string',
        'template': Template(str),
        'cases': (
            {'in': 'Hello', 'out': 'Hello'},
            {'in': str(), 'out': ''},
            {'in': DefaultValue, 'out': DefaultValue},
        ),
    },
    {
        'name': 'dict',
        'template': TemplateDict(user=Template(str), code=Template(int)),
        'cases': (
            {'in': None,
                'out': None},
            {'in': 123,
                'out': 123},
            {'in': {},
                'out': {}},
            {'in': {'user': 123},
                'out': {'user': 123}},
            {'in': {'user': None},
                'out': {'user': None}},
            {'in': {'user': DefaultValue},
                'out': {}},
            {'in': {'user': 'A10N'},
                'out': {'user': 'A10N'}},
            {'in': {'other': None},
                'out': {}},
            {'in': {'other': 'A10N'},
                'out': {}},
            {'in': {'user': 'A10N', 'other': 'A10N'},
                'out': {'user': 'A10N'}},
            {'in': {'user': 123, 'code': 'A10N'},
                'out': {'user': 123, 'code': 'A10N'}},
            {'in': {'user': 'A10N', 'code': 123},
                'out': {'user': 'A10N', 'code': 123}},
            {'in': {'user': 'A10N', 'code': 123, 'other': None},
                'out': {'user': 'A10N', 'code': 123}},
        ),
    },
    {
        'name': 'optional-no-default',
        'template': Optional(Template(str)),
        'cases': (
            {'in': None, 'out': None},
            {'in': 'string', 'out': 'string'},
            {'in': DefaultValue, 'out': DefaultValue},
        ),
    },
    {
        'name': 'optional-with-default',
        'template': Optional(Template(str), default='DEFAULT'),
        'cases': (
            {'in': None, 'out': None},
            {'in': 'string', 'out': 'string'},
            {'in': DefaultValue, 'out': 'DEFAULT'},
        ),
    },
    {
        'name': 'optional-dict',
        'template': TemplateDict(name=Optional(Template(str), default='Unknown')),
        'cases': (
            {'in': {}, 'out': {'name': 'Unknown'}},
            {'in': {'age': 17}, 'out': {'name': 'Unknown'}},
            {'in': {'name': 'Alon'}, 'out': {'name': 'Alon'}},
            {'in': {'name': 'Alon', 'age': 17}, 'out': {'name': 'Alon'}},
            {'in': None, 'out': None},
            {'in': DefaultValue, 'out': DefaultValue},
        ),
    },
    {
        'name': 'list',
        'template': TemplateList(Template(int, float)),
        'cases': (
            {'in': [], 'out': []},
            {'in': (), 'out': []},
            {'in': [1, 2.3, 4], 'out': [1, 2.3, 4]},
            {'in': (1.23,), 'out': [1.23]},
            {'in': [1, 'hello'], 'out': [1, 'hello']},
            # Even if value from wrong type, will dump the given data.
            {'in': None, 'out': None},
            {'in': 'NotAList', 'out': 'NotAList'}
        ),
    },
    {
        'name': 'list-of-dicts',
        'template': TemplateList(TemplateDict(user=Template(str), code=Template(int))),
        'cases': (
            {'in': None, 'out': None},
            {'in': [], 'out': []},
            {'in': [{'user': 'Alon', 'code': 123, 'another': True}],
                'out': [{'user': 'Alon', 'code': 123}]},
            {'in': [{'yes': True}, {'no': False}],
                'out': [{}, {}]},
            {'in': ['hello', {'hi': 'hello'}],
                'out': ['hello', {}]},
        )
    },
]


def generate_params():
    params = list()

    for test in cases:
        for case in test['cases']:
            params.append(pytest.param(
                test['template'],
                case['in'],
                case['out'],
                id=test.get('name'),
            ))

    return params


@pytest.mark.parametrize('template, iin, out', generate_params())
def test_dumps(template, iin, out):

    container = HeadContainer()
    template.container_dump(
        container=container,
        data=iin
    )

    if container.data != out:
        pytest.fail(
            'Container dump result unexpected\n'
            f"expected: '{out}'\n"
            f"got: '{container.data}'\n"
        )
