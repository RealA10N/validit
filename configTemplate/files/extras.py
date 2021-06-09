import typing
from configTemplate.exceptions import MissingExtras


class ExtraModules():
    """ A helper object that imports and stores extra modules. If one or more
    of the needed modules fails to import, raises a custom error. """

    def __init__(self,
                 class_name: str,
                 extra_name: str,
                 module_names: typing.List[str]
                 ) -> None:
        self._class_name = class_name
        self._extra_name = extra_name
        self._module_names = module_names

        self._modules = dict()
        self._imported = False

    def iimport(self):
        """ Tries to import the extra modules, and saves them locally.
        If one or more of the imports fails, raises a custom error. 
        If the modules are already imported, silently skips importing
        them again. """

        if self._imported:
            # If the given modules are already loaded, do not load them again
            return

        for module in self._module_names:
            try:
                # Try importing and saving the current module
                self._modules[module] = __import__(module)

            except ImportError as error:
                # If can't import, raise an error
                raise MissingExtras(
                    f"To use the '{self._class_name}' object you must install additional required packages. " +
                    f"Use 'pip install configTemplate[{self._extra_name}]'"
                ) from error

        # Finally, set the `imported` state to `True`
        self._imported = True

    def __getattr__(self, name):
        return self._modules.get(name)
