
class DefaultValue:
    """ A default value used in the `TemplateDict` object to indicate that the
    key is missing in the given data. """

    def __repr__(self):
        return "<DefaultValue>"


class AnyLength:
    """ A class that "contains everything". Will return `True` for any call
    to the `__contains__` method. Used as the default `valid_lengths` parameter
    to `TemplateList` check method, because with this object every list length
    is valid. """

    @staticmethod
    def __contains__(*_):
        return True
