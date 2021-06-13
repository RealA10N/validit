import pytest

from configTemplate.utils import DefaultValue
from configTemplate.containers import HeadContainer

from configTemplate import (
    Template,
    TemplateDict,
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
                'out': {}},
            {'in': 123,
                'out': {}},
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
            {'in': None, 'out': {'name': 'Unknown'}},
            {'in': DefaultValue, 'out': {'name': 'Unknown'}},
        ),
    }
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
