import typing
from abc import ABC, abstractmethod
from collections import defaultdict

from termcolor import colored

from .errors import TemplateCheckError


class TemplateCheckErrorManager(ABC):

    @abstractmethod
    def register_error(self, error: TemplateCheckError) -> None:
        pass


class TemplateCheckErrorCollection(TemplateCheckErrorManager):
    """ An object that collects errors and can display them to the user. """

    def __init__(self):
        self.groups = defaultdict(list)

    def __iter__(self,) -> typing.Iterator[TemplateCheckError]:
        return (
            error
            for error_group in self.groups.values()
            for error in error_group
        )

    def __len__(self,) -> int:
        """ Returns the number of registered errors """
        return self.count

    def __bool__(self,) -> bool:
        """ Returns `True` only if there are no errors registered """
        return self.no_errors

    def __repr__(self) -> str:
        """ Returns a colored string that shows the results of the check """
        if self.no_errors:
            return colored(
                'Data check resulted in ZERO errors!',
                'green', attrs=('bold',)
            )
        return '\n'.join(error.colored for error in self)

    @property
    def count(self,) -> int:
        """ Returns the number of registered errors """
        return len([error for error in self])

    @property
    def no_errors(self,) -> bool:
        """ Returns `True` only if there are zero errors registered """
        return self.count == 0

    def register_error(self, error: TemplateCheckError) -> None:
        """ Add an error to the collection. """
        self.groups[type(error)].append(error)


class TemplateCheckRaiseOnError(TemplateCheckErrorManager):

    def register_error(self, error: TemplateCheckError):
        raise error
