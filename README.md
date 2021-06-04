# configTemplate

[![Build](https://github.com/RealA10N/configTemplate/actions/workflows/build.yaml/badge.svg)](https://github.com/RealA10N/configTemplate/actions/workflows/build.yaml)
[![PyPI](https://img.shields.io/pypi/v/configTemplate)](https://pypi.org/project/configTemplate/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/configTemplate)](https://pypi.org/project/configTemplate/)
[![GitHub Repo stars](https://img.shields.io/github/stars/reala10n/configTemplate?style=social)](https://github.com/RealA10N/configTemplate)

_Easily define configuration file structures, and check if a given
configuration file matches the template._

## Installation

**configTemplate** is tested on CPython 3.6, 3.7, 3.8 and 3.9.

Simply install using pip:

```bash
pip install configTemplate
```

## Usage

To create a template, you will need the basic `Template` module, and usually the
other three basic modules `TemplateList`, `TemplateDict` and `TemplateOptional`.

```python
from configTemplate import Template, TemplateList, TemplateDict, TemplateOptional
```

Now, lets create a basic template that represents a single user:

```python
TemplateUser = TemplateDict(        # a dictionary with 2 required values
    username=Template(str),         # username must be a string
    passcode=Template(int, str),    # can be a string or an integer.
    nickname=TemplateOptional(str), # optional - if provided, must be a string.
)
```

Check if data matches your template using the `check` method:

```python
errors = TemplateUser.check({'username': 'RealA10N', 'passcode': 12345})
# the check method returns a `TemplateCheckErrorManager` instance
# read full documentation for more information.

if errors:
    print(f'Found {errors.count} conflicts:')
    print(errors)   # prints a detailed and colored error list

else:
    print('data follows the template!')
```

## Using configTemplate as a dependency

**configTemplate** is still under active development, and some core features
may change substantially in the near future.

If you are planning to use **configTemplate** as a dependency for your project,
we highly recommend to specify the exact version of the module you are using
in the `requirements.txt` file or `setup.py` scripts.

For example, to pinpoint version _v0.2.0_ use the following line in your
`requirements.txt` file:

```pip requirements
configTemplate==0.2.0
```
