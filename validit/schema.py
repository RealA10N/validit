from abc import ABC, abstractmethod


class Schema(ABC):

    @abstractmethod
    def validate(self, data):
        """ An abstract method that will validate the given data according to
        the current schema. This returns a generator that will yield
        'ValidationError' instances for every error in the data.
        The generator won't yield any values if the data is valid. """
