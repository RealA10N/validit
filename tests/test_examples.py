import os
import pytest

from configTemplate import (
    Template, TemplateList, TemplateDict,
    Validate, ValidateFromJSON, ValidateFromYAML, ValidateFromTOML
)

THIS = __file__
HERE = os.path.dirname(THIS)
EXAMPLES_FOLDER = os.path.join(HERE, 'examples')

VALIDATOR_EXTENSIONS = {
    '.json': ValidateFromJSON,
    '.yaml': ValidateFromYAML,
    '.toml': ValidateFromTOML,
}

cases = {
    'example1': TemplateDict(
        title=Template(str),
        owner=TemplateDict(
            name=Template(str),
            dob=Template(str),
        ),
        database=TemplateDict(
            server=Template(str),
            ports=TemplateList(Template(int)),
            connection_max=Template(int),
            enabled=Template(bool),
        ),
        clients=TemplateDict(
            data=TemplateList(
                TemplateList(Template(str, int)),
            ),
            hosts=TemplateList(Template(str)),
        ),
    )
}


def to_validator(name: str):
    for ext, validator in VALIDATOR_EXTENSIONS.items():
        if name.endswith(ext):
            return validator

    return None


def get_example_files():
    params = dict()

    for name in cases:
        folder = os.path.join(EXAMPLES_FOLDER, name)

        params[name] = {
            os.path.join(folder, file): to_validator(file)
            for file in os.listdir(folder)
            if to_validator(file) is not None
        }

    return params


@pytest.mark.parametrize('template, examples', [
    pytest.param(
        cases[name],
        value,
        id=name,
    )
    for name, value in get_example_files().items()
])
def test_matching_example_data(template, examples):

    data = list()
    for filepath, validator in examples.items():
        with open(filepath, 'r') as file:
            data.append(
                validator(template, file).data
            )

    for cur_data in data:
        if cur_data != data[0]:
            pytest.fail(
                'Data from different example files are not equal.'
            )


@ pytest.mark.parametrize('template, filepath, validator', [
    pytest.param(
        cases[name],
        filepath,
        validator,
        id=f'{name}-{validator.__name__}',
    )
    for name, info in get_example_files().items()
    for filepath, validator in info.items()
])
def test_no_validation_errors(template, filepath, validator):

    with open(filepath, 'r') as file:
        result: Validate = validator(template, file)

    if result.errors:
        pytest.fail(
            f'Found {result.errors.count} validation errors when expected none:\n' +
            str(result.errors)
        )
