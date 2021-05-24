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
        self.by_type = defaultdict(list)
        self.by_order = list()

    def register_error(self, error: TemplateCheckError):
        """ Add an error to the collection. """

        self.by_type[type(error)].append(error)
        self.by_order.append(error)

    def print_errors(self, group_by_type=False):
        """ Print the collected errors to the user. """

        errors = [
            error
            for error_group in self.by_type.values()
            for error in error_group
        ] if group_by_type else self.by_order

        for error in errors:
            print(error.description)


class TemplateCheckRaiseOnError(TemplateCheckErrorManager):

    def register_error(self, error: TemplateCheckError):
        raise error
