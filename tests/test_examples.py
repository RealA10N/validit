import typing
import os
import sys

import pytest
from collections import namedtuple

from validit import (
    Validate,
    ValidateFromJSON,
    ValidateFromYAML,
    ValidateFromTOML,
)

THIS = __file__
HERE = os.path.dirname(THIS)
TOP = os.path.join(HERE, os.pardir)
EXAMPLES_FOLDER = os.path.join(TOP, 'examples')

VALIDATOR_EXTENSIONS = {
    '.json': ValidateFromJSON,
    '.yaml': ValidateFromYAML,
    '.toml': ValidateFromTOML,
}

ExampleInfo = namedtuple('ExampleInfo', ['files', 'template'])


def to_validator(name: str):
    for ext, validator in VALIDATOR_EXTENSIONS.items():
        if name.endswith(ext):
            return validator

    return None


def get_example_files() -> typing.List[ExampleInfo]:
    params = list()

    examples = [
        name
        for name in os.listdir(EXAMPLES_FOLDER)
        if os.path.isdir(
            os.path.join(EXAMPLES_FOLDER, name)
        )
    ]

    for name in examples:
        folder = os.path.join(EXAMPLES_FOLDER, name)

        # Loading example files and corresponding validators
        files = {
            os.path.join(folder, file): to_validator(file)
            for file in os.listdir(folder)
            if to_validator(file) is not None
        }

        # Loading the template
        sys.path.append(folder)
        pyfile = next(
            name
            for name in os.listdir(folder)
            if name.endswith('.py')
        )
        filename = os.path.splitext(pyfile)[0]
        template = __import__(filename, fromlist=['__template__'])

        # Add the current example into the params list
        params.append(
            ExampleInfo(
                files=files,
                template=template.__template__
            )
        )

    return params


@pytest.mark.parametrize('template, examples', [
    pytest.param(
        info.template,
        info.files,
    )
    for info in get_example_files()
])
def test_matching_example_data(template, examples):

    data = list()
    for filepath, validator in examples.items():
        with open(filepath, 'r') as file:
            data.append(
                validator(template, file).data
            )

    if any(data[0] != ddata for ddata in data):
        pytest.fail(
            'Data from different example files are not equal.'
        )


@pytest.mark.parametrize('template, filepath, validator', [
    pytest.param(
        info.template,
        filepath,
        validator,
        id=os.path.basename(filepath)
    )
    for info in get_example_files()
    for filepath, validator in info.files.items()
])
def test_no_validation_errors(template, filepath, validator):

    with open(filepath, 'r') as file:
        result: Validate = validator(template, file)

    if result.errors:
        pytest.fail(
            f'Found {result.errors.count} validation errors when expected none:\n' +
            str(result.errors)
        )
