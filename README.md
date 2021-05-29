# configTemplate

[![Build](https://github.com/RealA10N/configTemplate/actions/workflows/build.yaml/badge.svg)](https://github.com/RealA10N/configTemplate/actions/workflows/build.yaml)

Easily define configuration file structures, and check if a given
configuration file matches the template.

## Usage

To create a template, you will need the basic `Template` module, and usually the
other two basic modules `TemplateList` and `TemplateDict`.

```python
from configTemplate import Template, TemplateList, TemplateDict
```

Now, lets create a basic template that represents a single user:

```python
TemplateUser = TemplateDict(    # a dictionary with 2 required values
    username=Template(str),     # username must be a string
    passcode=Template(int, str) # can be a string or an integer.
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

## Installation

**configTemplate** is tested on CPython 3.6, 3.7, 3.8 and 3.9.

Simply install using pip:

```bash
pip install configTemplate
```
