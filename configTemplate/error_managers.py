from abc import ABC, abstractmethod
from collections import defaultdict

from .errors import TemplateCheckError


class TemplateCheckErrorManager(ABC):

    @abstractmethod
    def register_error(self, error: TemplateCheckError):
        pass


class TemplateCheckErrorCollection(TemplateCheckErrorManager):
    """ An object that collects errors and can display them to the user. """

    def __init__(self):
        self.groups = defaultdict(list)

    def register_error(self, error: TemplateCheckError):
        """ Add an error to the collection. """
        self.groups[type(error)].append(error)

    def print_errors(self):
        """ Print the collected errors to the user. """

        for error_group in self.groups.values():
            for error in error_group:
                print(error.colored_description)


class TemplateCheckRaiseOnError(TemplateCheckErrorManager):

    def register_error(self, error: TemplateCheckError):
        raise error
