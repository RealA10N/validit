import textwrap


def shorten(text: str):
    """ If the given text is too long, cuts the end and replaces it with '...'. """
    return textwrap.shorten(text, width=25, placeholder='...')
