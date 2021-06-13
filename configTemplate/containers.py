import typing
from abc import ABC, abstractmethod

from configTemplate.utils import DefaultValue


class BaseContainer:

    @property
    @abstractmethod
    def data(self,):
        """ Returns the data that the container holds. """

    @data.setter
    @abstractmethod
    def data(self, value):
        """ Sets the data inside the container. """

    def __getitem__(self, index):
        """ Returns a new container instace that represents the data in from
        the current container in the given index. """
        return Container(parent=self, chiled=index)

    def __str__(self,) -> str:
        """ Returns a string with the stored data string representation. """
        return f'Container<{self.data}>'


class HeadContainer(BaseContainer):
    """ The head container. This is the root of the tree, and only this instance
    actually stores the data. All other instances just store pointers (in some
    way or another) to a part of the data in this container. """

    def __init__(self, data: typing.Any = DefaultValue):
        self.__data = data

    @property
    def data(self,):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value


class Container(BaseContainer):
    """ A regular container that stores data. """

    def __init__(self, parent: BaseContainer, chiled: typing.Union[str, int]):
        self.__parent = parent
        self.__chiled = chiled

    @property
    def data(self,):
        """ Returns the data that is stored in the container. If there is no
        data in the container, returns the `DefaultValue` object. """

        try:
            return self.__parent.data[self.__chiled]
        except LookupError:
            # If data doesn't exist
            return DefaultValue

    @data.setter
    def data(self, value) -> None:
        self.__parent.data[self.__chiled] = value
