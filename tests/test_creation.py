import pytest
from configTemplate import Template, TemplateDict, TemplateList
from configTemplate.exceptions import InvalidTemplateConfiguration


class ExampleObj: pass
class SonOfExample(ExampleObj): pass
class AnotherObj: pass


class TestBaseTemplate:

    @pytest.mark.parametrize('instance', (
        1, str(), bool(), ExampleObj(), SonOfExample(),
    ))
    def test_template_of_instance(self, instance):
        """ Test that a template of instance (and not a type) raises an
        error. """
        with pytest.raises(InvalidTemplateConfiguration):
            Template(instance)

    @pytest.mark.parametrize('types', (
        (ExampleObj,),
        (int, float, complex),
        (str, bool, AnotherObj),
        (ExampleObj, SonOfExample, AnotherObj),
    ))
    def test_template_creation(self, types):
        """ Test that a template constractor provided with one or more types
        can be initialized without errors. """
        Template(*types)


class TestTemplateDict:

    @pytest.mark.parametrize('template', (
        {'username': Template(str)},
        {
            'name': Template(str),
            'id': Template(int),
            'height': Template(int, float),
        },
    ))
    def test_dict_template_creation(self, template):
        TemplateDict(**template)

    @pytest.mark.parametrize('template', (
        {'typeNotTemplate': str},
        {'instance': 'hello!'},
    ))
    def test_dict_template_fails(self, template):
        with pytest.raises(InvalidTemplateConfiguration):
            TemplateDict(**template)
