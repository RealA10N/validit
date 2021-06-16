import typing

from dataclasses import dataclass, field
from termcolor import colored

from validit.errors.managers import TemplateCheckErrorCollection as ErrorCollection
from validit.templates.base import BaseTemplate
from validit.containers import HeadContainer
from validit.utils import ExtraModules

from validit.errors.parsing import (
    JsonParsingError,
    YamlParsingError,
    TomlParsingError,
)


@dataclass
class ValidateInformation:
    """ A dataclass that stores information about a validation check. 
    An instance of this object can be passed to the `Validate` constructor.
    If the `Validate` constructor recives raw data (which will happen most in
    most cases), it will convert the data to a `ValidateInformation` instance.
    """

    data: typing.Any = None
    errors: ErrorCollection = field(default_factory=ErrorCollection)
    fatal_error: bool = False


class Validate:

    def __init__(self,
                 template: BaseTemplate,
                 data: typing.Union[ValidateInformation, typing.Any]
                 ) -> None:
        """ Validate the given data with the given template. """

        if not isinstance(data, ValidateInformation):
            data = ValidateInformation(data=data)

        self._info: ValidateInformation = data
        self._data: HeadContainer = HeadContainer()
        self._template: BaseTemplate = template

        if not self._info.fatal_error:
            template.container_dump(self._data, self._info.data)
            template.validate(self._data, self._info.errors)

    @property
    def template(self,) -> BaseTemplate:
        """ Returns the template given to the constructor. """
        return self._template

    @property
    def errors(self,) -> ErrorCollection:
        """ Returns an error collection object that stores a collection
        of validation errors. """
        return self._info.errors

    @property
    def data(self,) -> typing.Any:
        """ The user data after it has been parsed. Data that is not required
        by the template is removed, and data that is not provided by the user
        but has a default value will be included. """
        return self._data.data

    @property
    def original(self,) -> typing.Any:
        """ The original user data, as given to the constructor. """
        return self._info.data

    def __str__(self,) -> str:
        return self.errors.__str__()


class ValidateFromFile(Validate):

    def __init__(self,
                 template: BaseTemplate,
                 data: ValidateInformation,
                 title: str = None,
                 ) -> None:
        """ Recives an open file (or file-like) object. Reads the data from it,
        parses it with the corresponding format and returns the validation
        results. """

        self.__title = title
        super().__init__(template, data)

    def __str__(self) -> str:
        """ Returns a string colored that represents the template error check
        results and errors with the given data. """

        additional = (colored(self.__title, 'cyan') + ' '
                      ) if self.__title else ''

        return '\n'.join(
            additional + line
            for line in super().__str__().splitlines()
        )


class ValidateFromJSON(ValidateFromFile):

    def __init__(self,
                 template: BaseTemplate,
                 fp: typing.IO,
                 title: str = None,
                 ) -> None:
        """ Validate data from a JSON file, using a user-made template. """

        extras = ExtraModules(
            class_name=self.__class__.__name__,
            extra_name='json',
            module_names=('json',),
        )

        info = ValidateInformation()

        try:
            info.data = extras.json.load(fp)

        except extras.json.JSONDecodeError as error:
            info.fatal_error = True
            info.errors.register_error(JsonParsingError(error))

        finally:
            super().__init__(template, info, title)


class ValidateFromYAML(ValidateFromFile):

    def __init__(self,
                 template: BaseTemplate,
                 fp: typing.IO,
                 title: str = None,
                 ) -> None:

        extras = ExtraModules(
            class_name=self.__class__.__name__,
            extra_name='yaml',
            module_names=('yaml',),
        )

        info = ValidateInformation()

        try:
            info.data = extras.yaml.full_load(fp)

        except extras.yaml.YAMLError as error:
            info.fatal_error = True
            info.errors.register_error(YamlParsingError(error))

        finally:
            super().__init__(template, info, title)


class ValidateFromTOML(ValidateFromFile):

    def __init__(self,
                 template: BaseTemplate,
                 fp: typing.IO,
                 title: str = None,
                 ) -> None:

        extras = ExtraModules(
            class_name=self.__class__.__name__,
            extra_name='toml',
            module_names=('toml',),
        )

        info = ValidateInformation()

        try:
            info.data = extras.toml.load(fp)

        except extras.toml.TomlDecodeError as error:
            info.fatal_error = True
            info.errors.register_error(TomlParsingError(error))

        finally:
            super().__init__(template, info, title)
