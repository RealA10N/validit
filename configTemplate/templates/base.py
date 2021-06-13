import typing
from abc import ABC, abstractmethod

from configTemplate.containers import BaseContainer
from configTemplate.utils import DefaultValue

from configTemplate.error_managers import (
    TemplateCheckErrorManager as ErrorManager,
    TemplateCheckErrorCollection as ErrorCollection,
)


class BaseTemplate(ABC):

    @abstractmethod
    def container_dump(self,
                       container: BaseContainer,
                       data: typing.Any = DefaultValue,
                       ) -> None:
        """ Recives an container and some data. Dumps only the relevent data
        (according to the template) into the container. The previously saved
        data in the container will be deleted. """

    @abstractmethod
    def check(self,
              container: BaseContainer,
              path: typing.Tuple[str] = tuple(),
              errors: ErrorManager = ErrorCollection(),
              ) -> ErrorManager:
        """ Preforms a validation check that validates if the given data
        follows the defined template. Returns an error manager object that
        contains a record of all mismatches. """
