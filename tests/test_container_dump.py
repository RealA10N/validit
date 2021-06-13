import pytest
from configTemplate import Template
from configTemplate.utils import DefaultValue
from configTemplate.containers import HeadContainer

cases = [
    {
        'name': 'base-template',
        'template': Template(str),
        'cases': (
            {'in': 'Hello', 'out': 'Hello'},
            {'in': str(), 'out': ''},
            {'in': DefaultValue, 'out': DefaultValue},
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
                id=test['name'],
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
