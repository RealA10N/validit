import typing
from abc import ABC, abstractmethod
from validit.utils import DefaultValue


class BaseContainer(ABC):

    @property
    @abstractmethod
    def data(self,):
        """ Returns the data that the container holds. """

    @data.setter
    @abstractmethod
    def data(self, value):
        """ Sets the data inside the container. """

    @property
    @abstractmethod
    def path(self,) -> typing.Tuple[typing.Union[str, int]]:
        """ Returns a tuple that represents the path taken from the head container
        to the current one. If the current container is the head container, will
        return an empty tuple. """

    def __getitem__(self, index):
        """ Returns a new container instace that represents the data in from
        the current container in the given index. """
        return Container(parent=self, chiled=index)

    def __iter__(self,):
        return ContainerIterator(self)

    def __str__(self,) -> str:
        """ Returns a string with the stored data string representation. """
        return f'Container<{self.data}>'


class ContainerIterator:
    """ An iterator that loops over a container and yields its
    container-children. """

    def __init__(self, container: BaseContainer):
        self.__container = container

        # By default, will use the iterator of the data to pass into __getitem__
        # This is the default behavior of a dictionray, because the iterator of
        # a dict return its keys (and they are passed to __getitem__ to retrive
        # values). Handling the special case of lists and tuples (which the
        # iterator yields the values and not the indices) will be done separately.

        if isinstance(container.data, (list, tuple)):
            self.__items = iter(range(len(container.data)))

        else:
            self.__items = iter(container.data)

    def __next__(self,):
        item = next(self.__items)
        return self.__container[item]


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

    @property
    def path(self,):
        return ()


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

    @property
    def path(self,):
        return self.__parent.path + (self.__chiled,)
