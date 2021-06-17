class ValidItError(Exception):
    """ The base exception for this module. """


class MissingExtras(ValidItError):
    """ Raised when trying to use extra features without installing the
    required packages (for example, trying to load YAML or TOML files without
    installing required extra packages). """


class InvalidTemplateConfiguration(ValidItError):
    """ Raised when a template configuration is not valid. """


class InvalidDefaultValue(ValidItError):
    """ Raised when the given default value doesn't match the given template.
    Used with the `Optional` object. """
