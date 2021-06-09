import typing
from abc import ABC

from termcolor import colored

from configTemplate import Template
from configTemplate.error_managers import TemplateCheckErrorCollection as ErrorCollection
from configTemplate.exceptions import MissingExtras

from .extras import ExtraModules


class TemplateFileLoader(ABC):

    _EXTRAS: ExtraModules

    def __init__(self,
                 template: Template,
                 fp: typing.TextIO,
                 title: str = None,
                 ) -> None:
        self._template = template
        self._fp = fp
        self._title = title
        self._data, self._errors, self._load_error = None, None, None

        self._EXTRAS.iimport()

    @property
    def data(self):
        """ Returns the loaded data from the configuration file, regardless if
        the template check passes or not. """
        return self._data

    @property
    def errors(self) -> ErrorCollection:
        """ Returns an `TemplateCheckErrorCollection` object that contains the
        results of the data template check for the loaded data from the
        configuration file, with the given template. """
        return self._errors

    def __repr__(self) -> str:
        """ Returns a string colored that represents the template error check
        results and errors with the given data. """

        additional = colored(self._title, 'cyan') + ' ' if self._title else ''

        if self._load_error:
            return additional + colored(self._load_error, 'red')

        errors_str = self.errors.__repr__()

        return '\n'.join(
            additional + line
            for line in errors_str.splitlines()
        )


class JsonFileLoader(TemplateFileLoader):

    _EXTRAS = ExtraModules(
        class_name='JsonFileLoader',
        extra_name='json',
        module_names=['json', ]
    )

    def __init__(self,
                 template: Template,
                 fp: typing.TextIO,
                 title: str = None,
                 ) -> None:
        """ Recives a file text stream and loads the data from the stream as if
        it is a json file. Automatically runs a template data check with the
        given template, and saves the error returns in the `errors` property. """
        super().__init__(template, fp, title=title)
        json = self._EXTRAS.json

        try: self._data = json.load(fp)
        except json.JSONDecodeError:
            self._load_error = 'failed to parse JSON file'

        self._errors = template.check(self._data)


class YamlFileLoader(TemplateFileLoader):

    _EXTRAS = ExtraModules(
        class_name='YamlFileLoader',
        extra_name='yaml',
        module_names=['yaml', ]
    )

    def __init__(self,
                 template: Template,
                 fp: typing.TextIO,
                 title: str = None,
                 ) -> None:
        """ Recives a file text stream and loads the data from the stream as if
        it is a yaml file. Automatically runs a template data check with the
        given template, and saves the error returns in the `errors` property. """
        super().__init__(template, fp, title=title)
        yaml = self._EXTRAS.yaml

        try: self._data = yaml.full_load(fp)
        except yaml.YAMLError:
            self._load_error = 'failed to parse YAML file'

        self._errors = template.check(self._data)


class TomlFileLoader(TemplateFileLoader):

    _EXTRAS = ExtraModules(
        class_name='TomlFileLoader',
        extra_name='toml',
        module_names=['toml', ]
    )

    def __init__(self,
                 template: Template,
                 fp: typing.TextIO,
                 title: str = None,
                 ) -> None:
        """ Recives a file text stream and loads the data from the stream as if
        it is a yaml file. Automatically runs a template data check with the
        given template, and saves the error returns in the `errors` property. """
        super().__init__(template, fp, title=title)
        toml = self._EXTRAS.toml

        try: self._data = toml.load(fp)
        except toml.decoder.TomlDecodeError:
            self._load_error = 'failed to parse TOML file'

        self._errors = template.check(self._data)
