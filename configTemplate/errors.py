import typing
from collections import defaultdict


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

        return ''.join(f'[{element}]' for element in self.path)

    @property
    def description(self,) -> str:
        """ Generates and returns a string that represents the current template
        check error. """
        msg = f'{self.path_str} - ' if self.path else str()
        msg += self.msg if self.msg else str()
        return msg


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
            msg=f"Expected {self.expected_str}, got '{self.got_str}'",
        )

    @property
    def expected_str(self,) -> str:
        """ A string that represents the expected type """
        formatname = lambda name: f"'{name.__name__}'"

        start, last = self.expected[:-1], self.expected[-1]
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


class TemplateCheckErrorCollection:
    """ An object that collects errors and can display them to the user. """

    def __init__(self):
        self.by_type = defaultdict(list)
        self.by_order = list()

    def add_error(self, error: TemplateCheckError):
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
