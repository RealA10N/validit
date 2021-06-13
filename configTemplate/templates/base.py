import typing
from abc import ABC, abstractmethod

from configTemplate.error_managers import TemplateCheckErrorManager
from configTemplate.containers import BaseContainer
from configTemplate.utils import DefaultValue


class BaseTemplate(ABC):

    @abstractmethod
    def check(self,
              data: typing.Any = DefaultValue,
              path: typing.Tuple[str] = tuple(),
              errors: ErrorManager = ErrorCollection(),
              ) -> ErrorManager:
        """ Preforms a validation check that validates if the given data
        follows the defined template. Returns an error manager object that
        contains a record of all mismatches. """
