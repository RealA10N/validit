import typing
from abc import ABC, abstractmethod
from termcolor import colored

from .errors import TemplateCheckError


class TemplateCheckErrorManager(ABC):

    @abstractmethod
    def register_error(self, error: TemplateCheckError) -> None:
        pass


class TemplateCheckErrorCollection(TemplateCheckErrorManager):
    """ An object that collects errors and can display them to the user. """

    def __init__(self):
        self.errors = list()

    def __iter__(self,) -> typing.Iterator[TemplateCheckError]:
        return (error for error in self.errors)

    def __len__(self,) -> int:
        """ Returns the number of registered errors """
        return self.count

    def __bool__(self,) -> bool:
        """ Returns `True` only if there are errors registered """
        return self.count != 0

    def __str__(self) -> str:
        """ Returns a colored string that shows the results of the check """
        return '\n'.join(error.__str__() for error in self)

    @property
    def count(self,) -> int:
        """ Returns the number of registered errors """
        return len([error for error in self])

    def register_error(self, error: TemplateCheckError) -> None:
        """ Add an error to the collection. """
        self.errors.append(error)

    def dump_errors(self, destination: TemplateCheckErrorManager):
        """ Dumps each error in the current error collection into the given
        error manager. """

        for error in self:
            destination.register_error(error)


class TemplateCheckRaiseOnError(TemplateCheckErrorManager):

    def register_error(self, error: TemplateCheckError):
        raise error
