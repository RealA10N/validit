import typing
import re

from termcolor import colored
from validit.utils import ExtraModules


class TemplateCheckError(Exception):
    """ A general object that represents a template check error.
    Although you can create instances of it, it is highly recommended to use
    subclasses of it to better describe the check error. """

    def __init__(self, path: typing.List[str], msg: str = None):
        self.path = path
        self.msg = msg

        super().__init__(self.description)

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

    def __init__(self, path):
        super().__init__(path, msg='Missing required information')


class TemplateCheckInvalidDataError(TemplateCheckError):
    """ An object that represents a template check error in which the expected
    data was found, but it didn't follow the expected format / type. """

    def __init__(self, path, expected: typing.Tuple[type], got: type):
        self.expected = expected
        self.got = got

        super().__init__(
            path,
            msg=f"Expected {self.expected_str} but got '{self.got_str}'",
        )

    @property
    def expected_str(self,) -> str:
        """ A string that represents the expected type """
        formatname = lambda name: f"'{name.__name__}'"

        excepted = list(self.expected)
        start, last = excepted[:-1], excepted[-1]
        string = ', '.join(formatname(type_) for type_ in start)

        if string:
            string += ' or '

        string += formatname(last)
        return string

    @property
    def got_str(self,) -> str:
        """ A string that represents the given type """
        got = self.got
        if not isinstance(got, type):
            got = type(got)
        return got.__name__


class TemplateCheckListLengthError(TemplateCheckError):
    """ An object that represents a template check error in which a given list
    has an invalid length according to the template configuration. """

    def __init__(self, path, expected: typing.Any, got: int):
        super().__init__(
            path,
            f'List length {got} is not in {expected}',
        )
