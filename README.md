# validit <!-- omit in toc -->

[![Test](https://img.shields.io/github/workflow/status/reala10n/validit/%E2%9C%94%20Test?label=test)](https://github.com/RealA10N/validit/actions/workflows/test.yaml)
[![PyPI](https://img.shields.io/pypi/v/validit)](https://pypi.org/project/validit/)

_Easily define configuration file structures, and validate files using the templates. 🍒📂_

- [Installation](#installation)
- [Usage](#usage)
  - [Defining a schema](#defining-a-schema)

## Installation

**validit** is tested on CPython 3.6 - 3.10.
Simply install using pip:

```bash
$ (sudo) pip install validit
```

## Usage

### Defining a schema

**validit** uses Python objects for constructing the Schema.
We provide a handful collection of Schema classes that should cover all your
basic usage cases, especially if you are going to validate a JSON, TOML or a YAML configuration file.
We will briefly talk about how you can create your own Schema objects later.

The classes that we provide for defining schemas are:

Name                 | Description
---------------------|-------------------------------------------------------------
`validit.String`     | Validates a string and matches it with a _RegEx_ pattern.
`validit.Number`     | Validates any real number in a certain range.
`validit.Integer`    | Validates an integer in a certain range.
`validit.Union`      | Matches a value with at least one schema.
`validit.Dictionary` | Validates a dictionary and all values inside it recursively.
`validit.Optional`   | Converts a field inside a `Dictionary` into an optional one.

