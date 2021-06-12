""" Test the creation of a template structure. """

import pytest
from configTemplate import Template, TemplateDict, TemplateList, Optional
from configTemplate.exceptions import InvalidTemplateConfiguration


class ExampleObj: pass
class SonOfExample(ExampleObj): pass
class AnotherObj: pass


VALID_BASE_TYPES = (
    (ExampleObj,),
    (int, float, complex),
    (str, bool, AnotherObj),
    (ExampleObj, SonOfExample, AnotherObj),
)

INVALID_TYPES = (
    1, str(), bool(), ExampleObj(), SonOfExample(),
    (str, int()),
    (bool, int, float, 'str'),
    (AnotherObj, ExampleObj(), SonOfExample()),
)


class TestBaseTemplate:

    @pytest.mark.parametrize('template', VALID_BASE_TYPES)
    def test_creation(self, template):
        """ Test that a template constractor provided with one or more types
        can be initialized without errors. """
        Template(*template)

    @pytest.mark.parametrize('template', INVALID_TYPES)
    def test_creation_fails(self, template):
        """ Test that a template of instance (and not a type) raises an
        error. """
        with pytest.raises(InvalidTemplateConfiguration):
            Template(template)


class TestTemplateOptional:
    @pytest.mark.parametrize('template', VALID_BASE_TYPES)
    def test_creation(self, template):
        """ Test that a template constractor provided with one or more types
        can be initialized without errors. """
        Optional(Template(*template))

    @pytest.mark.parametrize('template', (
        Template(str), Template(int, str),
        TemplateDict(user=Template(str), password=Template(int)),
        TemplateList(Template(str)),
        TemplateDict(user=Template(ExampleObj), password=Template(AnotherObj)),
    ))
    def test_complex_creation(self, template):
        """ Test that a optional template constractor accepts advance templates
        like dictionary template and list template. """
        Optional(template)

    @ pytest.mark.parametrize('template', INVALID_TYPES)
    def test_creation_fails(self, template):
        """ Test that a template of instance (and not a type) raises an
        error. """
        with pytest.raises(InvalidTemplateConfiguration):
            Optional(template)


class TestTemplateDict:

    @ pytest.mark.parametrize('template', (
        {'username': Template(str)},
        {
            'name': Template(str),
            'id': Template(int),
            'height': Template(int, float),
        },
    ))
    def test_creation(self, template):
        TemplateDict(**template)

    @ pytest.mark.parametrize('template', (
        {'typeNotTemplate': str},
        {'instance': 'hello!'},
        {'string': Template(str),
         'object': ExampleObj,
         }
    ))
    def test_creation_fails(self, template):
        with pytest.raises(InvalidTemplateConfiguration):
            TemplateDict(**template)


class TestTemplateList:

    @ pytest.mark.parametrize('template', (
        Template(int),
        Template(str),
        Template(int, float, complex),
        Template(str, ExampleObj, AnotherObj),
        TemplateDict(username=Template(str), secretcode=Template(int)),
        TemplateList(Template(int)),
    ))
    def test_creation(self, template):
        TemplateList(template)

    @ pytest.mark.parametrize('template', (
        int, str, 'astring', ExampleObj, SonOfExample(), AnotherObj,
    ))
    def test_creation_fails(self, template):
        with pytest.raises(InvalidTemplateConfiguration):
            TemplateList(template)

    @pytest.mark.parametrize('types', VALID_BASE_TYPES)
    @pytest.mark.parametrize('lengths', (
        range(10), range(82), range(20, 32, 3),
        {1, 2}, [1, 2, 3], [i for i in range(10_000)]
    ))
    def test_length(self, types, lengths):
        TemplateList(Template(*types), valid_lengths=lengths)

    @pytest.mark.parametrize('types', VALID_BASE_TYPES)
    @pytest.mark.parametrize('lengths', (
        10, 0, range,
    ))
    def test_length_fails(self, types, lengths):
        with pytest.raises(InvalidTemplateConfiguration):
            TemplateList(Template(*types), valid_lengths=lengths)
