import typing
from validit.exceptions import MissingExtras


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

    @staticmethod
    def __repr__() -> str:
        return 'AnyLength'


class ExtraModules:
    """ A helper object that imports and stores extra modules. If one or more
    of the needed modules fails to import, raises a custom error. """

    def __init__(self,
                 class_name: str,
                 extra_name: str,
                 module_names: typing.List[str]
                 ) -> None:
        """ Tries to import the extra modules, and saves them locally.
        If one or more of the imports fails, raises a custom error. """
        self._modules = dict()

        for module in module_names:
            try:
                # Try importing and saving the current module
                self._modules[module] = __import__(module)

            # If can't import, raise an error
            except ImportError as error:
                raise MissingExtras(
                    f"To use the '{class_name}' object you must install additional required packages. " +
                    f"Use 'pip install validit[{extra_name}]'"
                ) from error

    def __getattr__(self, name):
        return self._modules.get(name)
