# validit <!-- omit in toc -->

[![Test](https://img.shields.io/github/workflow/status/reala10n/validit/%E2%9C%94%20Test?label=test)](https://github.com/RealA10N/validit/actions/workflows/test.yaml)
[![PyPI](https://img.shields.io/pypi/v/validit)](https://pypi.org/project/validit/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/validit)](https://pypi.org/project/validit/)
[![GitHub Repo stars](https://img.shields.io/github/stars/reala10n/validit?style=social)](https://github.com/RealA10N/validit)

_Easily define configuration file structures, and validate files using the templates. 🍒📂_

- [Installation](#installation)
  - [Support for additional file formats](#support-for-additional-file-formats)
- [Usage](#usage)
  - [Defining a template](#defining-a-template)
  - [Validating data](#validating-data)
    - [Validating data from files](#validating-data-from-files)
- [Using validit as a dependency](#using-validit-as-a-dependency)

## Installation

**validit** is tested on CPython 3.6, 3.7, 3.8, and 3.9.
Simply install using pip:

```bash
$ (sudo) pip install validit
```

### Support for additional file formats

By default, _validit_ only supports `JSON` configuration files, or
already loaded data (not directly from a configuration file). However, using
additional dependencies, _validit_ supports the following file formats:

- `JSON`
- `YAML`
- `TOML`

To install _validit_ with the additional required dependencies to support
your preferred file format, use:

```yaml
pip install validit[yaml]        # install dependencies for yaml files
pip install validit[toml]        # toml files
pip install validit[json,toml]   # json and toml files
pip install validit[all]         # all available file formats
```

## Usage

### Defining a template

To create a template, you will need the basic `Template` module, and usually the
other three basic modules `TemplateList`, `TemplateDict`, and `Optional`.

In the following example, we will create a basic template that represents a single user:

```python
from validit import Template, TemplateList, TemplateDict, Optional

TemplateUser = TemplateDict(            # a dictionary with 2 required values
    username=Template(str),             # username must be a string
    passcode=Template(int, str),        # can be a string or an integer.
    nickname=Optional(Template(str)),   # optional - if provided, must be a string.
)
```

### Validating data

To validate your data with a template, you should use the `Validate` object.

```python
from validit import Template, TemplateDict, Optional, Validate

template = TemplateDict(
    username=Template(str),
    passcode=Template(int, str),
    nickname=Optional(Template(str)),
)

data = {
    'username': 'RealA10N',
    'passcode': 123,
}

valid = Validate(template, data)
if valid.errors:            # if one or more errors found
    print(valid.errors)     # print errors to console
    exit(1)                 # exit the script with exit code 1

else:                       # if data matches the template
    run_script(valid.data)  # run the script with the loaded data
```

#### Validating data from files

If your data is stored in a file, it is possible to use the `ValidateFromJSON`,
`ValidateFromYAML` or `ValidateFromTOML` objects instead:

```python
from validit import Template, TemplateDict, Optional, ValidateFromYAML

filepath = '/path/to/data.yaml'
template = TemplateDict(
    username=Template(str),
    passcode=Template(int, str),
    nickname=Optional(Template(str)),
)

with open(filepath, 'r') as file:
    # load and validate data from the file
    valid = ValidateFromYAML(file, template)
    
if valid.errors:            # if one or more errors found
    print(valid.errors)     # print errors to console
    exit(1)                 # exit the script with exit code 1

else:                       # if data matches the template
    run_script(valid.data)  # run the script with the loaded data
```

## Using validit as a dependency

_validit_ is still under active development, and some core features
may change substantially in the near future.

If you are planning to use _validit_ as a dependency for your project,
we highly recommend specifying the exact version of the module you are using
in the `requirements.txt` file or `setup.py` scripts.

For example, to pinpoint version _v1.3.0_ use the following line in your
`requirements.txt` file:

```yaml
validit==1.3.0
validit[yaml]==1.3.0     # If using extra file formats
```
