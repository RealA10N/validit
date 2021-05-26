class InvalidTemplateConfiguration(Exception):
    """ Raised when a template configuration is not valid. """


class InvalidLengthRange(InvalidTemplateConfiguration, TypeError):
    """ Raised when a function expects a length range as a `range` instance,
    but recives something else. """
