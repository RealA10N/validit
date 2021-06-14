import typing

from dataclasses import dataclass
from termcolor import colored

from configTemplate.errors.managers import TemplateCheckErrorCollection as ErrorCollection
from configTemplate.templates.base import BaseTemplate
from configTemplate.containers import HeadContainer
from configTemplate.utils import ExtraModules


@dataclass
class ValidateInformation:
    """ A dataclass that stores information about a validation check. 
    An instance of this object can be passed to the `Validate` constructor.
    If the `Validate` constructor recives raw data (which will happen most in
    most cases), it will convert the data to a `ValidateInformation` instance.
    """

    data: typing.Any = None
    errors: ErrorCollection = ErrorCollection()
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
