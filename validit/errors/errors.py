import typing
import re

from termcolor import colored
from validit.containers import BaseContainer


def readable_list(items: typing.List[str]) -> str:
    """ Converts a list of strings into a comma seperated list. """

    if not items:
        return str()

    body, end = items[:-1], items[-1]
    s = ', '.join(repr(cur) for cur in body)

    if s:
        s += ' or '

    return s + repr(end)


class TemplateCheckError(Exception):
    """ A general object that represents a template check error.
    Although you can create instances of it, it is highly recommended to use
    subclasses of it to better describe the check error. """

    def __init__(self,
                 container: BaseContainer = None,
                 msg: str = None,
                 ) -> None:
        self.container = container
        self.msg = msg

        super().__init__(self.description)

    @property
    def path(self,) -> typing.Tuple[str]:
        """ A collection of strings that represents the path from the main data
        to the area in which the current error occurred. """
        return self.container.path if self.container else ()

    @property
    def path_str(self,) -> str:
        """ A string that represents the path where the template check error
        occurred. """

        return colored(
            ''.join(f'[{element}]' for element in self.path),
            'yellow'
        ) if self.path else ''

    @property
    def description(self,) -> str:
        """ Generates and returns a string that represents the current template
        check error. """
        return colored(self.msg, 'red') if self.msg else ''

    def __str__(self,) -> str:
        """ Generates and returns a colors string that represents the current
        template check error. """

        spacing = ' ' if self.description and self.path_str else ''
        return f'{self.path_str}{spacing}{self.description}'

    @property
    def no_color_str(self,) -> str:
        """ A string non colored string that represents the current template
        error. """
        return re.sub('\033\\[([0-9]+)(;[0-9]+)*m', '', str(self))


class TemplateCheckMissingDataError(TemplateCheckError):
    """ An object that represents a template check error in which some required
    data is missing. """

    def __init__(self, container: BaseContainer) -> None:
        super().__init__(container, msg='Missing required information')


class TemplateCheckInvalidOptionError(TemplateCheckError):

    def __init__(self,
                 container: BaseContainer,
                 expected: tuple,
                 got: typing.Any,
                 ) -> None:
        self.expected = expected
        self.got = got

        super().__init__(
            container,
            msg=f"Expected {readable_list(expected)} but got {repr(got)}"
        )


class TemplateCheckInvalidDataError(TemplateCheckError):
    """ An object that represents a template check error in which the expected
    data was found, but it didn't follow the expected format / type. """

    def __init__(self,
                 container: BaseContainer,
                 expected: typing.Tuple[type],
                 got: type
                 ) -> None:
        self.expected = expected
        self.got = got

        expected_str = readable_list([cls.__name__ for cls in expected])
        got_type = type(got) if not isinstance(got, type) else got
        got_str = repr(got_type.__name__)

        super().__init__(
            container,
            msg=f"Expected {expected_str} but got {got_str}",
        )


class TemplateCheckListLengthError(TemplateCheckError):
    """ An object that represents a template check error in which a given list
    has an invalid length according to the template configuration. """

    def __init__(self, container: BaseContainer, expected: typing.Any, got: int):
        super().__init__(
            container,
            f'List length {got} is not {expected!r}',
        )
