import pytest

from configTemplate.utils import DefaultValue
from configTemplate.containers import HeadContainer

from configTemplate import (
    Template,
    TemplateDict,
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
