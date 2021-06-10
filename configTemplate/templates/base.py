import typing
from abc import ABC, abstractmethod

from configTemplate.error_managers import (
    TemplateCheckErrorManager,
    TemplateCheckErrorCollection as ErrorCollection,
)

ErrorManager = typing.TypeVar('ErrorManager', bound=TemplateCheckErrorManager)


class DefaultValue:
    """ A default value used in the `TemplateDict` object to indicate that the
    key is missing in the given data. """

    def __repr__(self): return "DefaultValue"


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
