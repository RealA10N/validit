# validit

[![Test](https://img.shields.io/github/workflow/status/reala10n/validit/%E2%9C%94%20Test?label=test)](https://github.com/RealA10N/validit/actions/workflows/test.yaml)
[![PyPI](https://img.shields.io/pypi/v/validit)](https://pypi.org/project/validit/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/validit)](https://pypi.org/project/validit/)
[![GitHub Repo stars](https://img.shields.io/github/stars/reala10n/validit?style=social)](https://github.com/RealA10N/validit)

_Easily define configuration file structures, and check if a given
configuration file matches the template._

## Installation

**validit** is tested on CPython 3.6, 3.7, 3.8, and 3.9.
Simply install using pip:

```bash
pip install validit
```

### Support for additional file formats

By default, _validit_ only supports `JSON` configuration files, or
already loaded data (not directly from a configuration file). However, using
additional dependencies, _validit_ supports the following file formats:

- JSON
- YAML
- TOML

To install _validit_ with the additional required dependencies to support
your preferred file format, use:

```yaml
pip install validit[yaml]        # install dependencies for yaml files
pip install validit[toml]        # toml files
pip install validit[json,toml]   # json and toml files
pip install validit[all]         # all available file formats
```

## Usage

To create a template, you will need the basic `Template` module, and usually the
other three basic modules `TemplateList`, `TemplateDict`, and `Optional`.

```python
from validit import Template, TemplateList, TemplateDict, Optional
```

Now, let's create a basic template that represents a single user:

```python
TemplateUser = TemplateDict(            # a dictionary with 2 required values
    username=Template(str),             # username must be a string
    passcode=Template(int, str),        # can be a string or an integer.
    nickname=Optional(Template(str)),   # optional - if provided, must be a string.
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

## Using validit as a dependency

_validit_ is still under active development, and some core features
may change substantially in the near future.

If you are planning to use _validit_ as a dependency for your project,
we highly recommend specifying the exact version of the module you are using
in the `requirements.txt` file or `setup.py` scripts.

For example, to pinpoint version _v0.3.2_ use the following line in your
`requirements.txt` file:

```yaml
validit==0.3.2
validit[yaml]==0.3.2     # If using extra file formats
```
