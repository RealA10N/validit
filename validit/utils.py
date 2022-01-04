import textwrap


def shorten(text: str):
    """ If the given text is too long, cuts the end and replaces it with '...'. """
    return textwrap.shorten(text, width=25, placeholder='...')


class MISSING:
    """ A dummy class that is uses with different 'get' methods as a default value
    when the requested value is missing. Used instead of the builtin 'None'. """
