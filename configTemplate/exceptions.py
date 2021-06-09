class ConfigTemplateError(Exception):
    """ The base exception for this module. """


class MissingExtras(ConfigTemplateError):
    """ Raised when trying to use extra features without installing the
    required packages (for example, trying to load YAML or TOML files without
    installing required extra packages). """


class InvalidTemplateConfiguration(ConfigTemplateError):
    """ Raised when a template configuration is not valid. """


class InvalidLengthRange(InvalidTemplateConfiguration, TypeError):
    """ Raised when a function expects a length range as a `range` instance,
    but recives something else. """
