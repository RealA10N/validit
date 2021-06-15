import typing
from abc import ABC, abstractmethod

from validit.containers import BaseContainer
from validit.utils import DefaultValue

from validit.errors.managers import (
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
    def validate(self,
                 container: BaseContainer,
                 errors: ErrorManager,
                 ) -> None:
        """ Preforms a validation check that validates if the given data
        follows the defined template. Returns an error manager object that
        contains a record of all mismatches. """
