""" Test the creation of a template structure. """

import pytest
from configTemplate import Template, TemplateDict, TemplateList
from configTemplate.exceptions import (
    InvalidTemplateConfiguration,
    InvalidLengthRange,
)


class ExampleObj: pass
class SonOfExample(ExampleObj): pass
class AnotherObj: pass


class TestBaseTemplate:

    @pytest.mark.parametrize('template', (
        (ExampleObj,),
        (int, float, complex),
        (str, bool, AnotherObj),
        (ExampleObj, SonOfExample, AnotherObj),
    ))
    def test_creation(self, template):
        """ Test that a template constractor provided with one or more types
        can be initialized without errors. """
        Template(*template)

    @pytest.mark.parametrize('template', (
        1, str(), bool(), ExampleObj(), SonOfExample(),
        (str, int()),
        (bool, int, float, 'str'),
        (AnotherObj, ExampleObj(), SonOfExample()),
    ))
    def test_creation_fails(self, template):
        """ Test that a template of instance (and not a type) raises an
        error. """
        with pytest.raises(InvalidTemplateConfiguration):
            Template(template)


class TestTemplateDict:

    @pytest.mark.parametrize('template', (
        {'username': Template(str)},
        {
            'name': Template(str),
            'id': Template(int),
            'height': Template(int, float),
        },
    ))
    def test_creation(self, template):
        TemplateDict(**template)

    @pytest.mark.parametrize('template', (
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

    @pytest.mark.parametrize('template', (
        (int,),
        (str,),
        (int, float, complex),
        (str, ExampleObj, AnotherObj),
    ))
    def test_creation(self, template):
        TemplateList(*template)

    @pytest.mark.parametrize('template', (
        (complex, int, 3.23),
        ('astring',),
        (ExampleObj, SonOfExample(), AnotherObj,),
    ))
    def test_creation_fails(self, template):
        with pytest.raises(InvalidTemplateConfiguration):
            TemplateList(*template)

    @pytest.mark.parametrize('template, length', (
        ((int, float), range(10)),
        ((str,), range(82)),
        ((ExampleObj, AnotherObj), range(20, 32, 3)),
    ))
    def test_length(self, template, length):
        TemplateList(*template, length=length)

    @pytest.mark.parametrize('template, length', (
        ((int, float), 10),
        ((str,), 0),
        ((ExampleObj, AnotherObj), range),
    ))
    def test_length_fails(self, template, length):
        with pytest.raises(InvalidLengthRange):
            TemplateList(*template, length=length)
