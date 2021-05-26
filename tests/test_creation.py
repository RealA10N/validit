import pytest
from configTemplate import Template, TemplateDict, TemplateList
from configTemplate.exceptions import InvalidTemplateConfiguration


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
    ))
    def test_creation_fails(self, template):
        with pytest.raises(InvalidTemplateConfiguration):
            TemplateDict(**template)
