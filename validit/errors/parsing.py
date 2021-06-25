import typing
from .errors import TemplateCheckError


class FileParsingError(TemplateCheckError):
    """ Raised or registered into a error manager when a data file is not
    formatted correctly and is invalid. """

    def __init__(self,
                 filetype: str = None,
                 msg: str = None,
                 pos: typing.Tuple[int, int] = None,
                 ):

        if filetype:
            string = f'Failed to parse {filetype} file'
        else:
            string = 'Failed to parse file'

        if msg:
            string += f': {msg}'

        if pos:
            string += f' (line {pos[0]} column {pos[1]})'

        super().__init__(msg=string)


class JsonParsingError(FileParsingError):
    """ Raised or registered into a error manager when a JSON file is not
    formatted correctly and is invalid. """

    def __init__(self, exception):
        """ Recives a `json.JSONDecodeError` error and passes it to the file
        parsing error constructor. """

        super().__init__(
            filetype='JSON',
            msg=exception.msg,
            pos=(exception.lineno, exception.colno),
        )


class YamlParsingError(FileParsingError):
    """ Raised or registered into a error manager when a YAML file is not
    formatted correctly and is invalid. """

    def __init__(self, exception):
        """ Recives a `yaml.YAMLError` error and passes it to the file
        parsing error constructor. """

        super().__init__(
            filetype='YAML',
            msg=exception.problem,
            pos=(
                exception.problem_mark.line,
                exception.problem_mark.column
            ),
        )


class TomlParsingError(FileParsingError):
    """ Raised or registered into a error manager when a YAML file is not
    formatted correctly and is invalid. """

    def __init__(self, exception):
        """ Recives a `toml.TomlDecodeError` error and passes it to the file
        parsing error constructor. """

        super().__init__(
            filetype='TOML',
            msg=exception.msg,
            pos=(exception.lineno, exception.colno),
        )
