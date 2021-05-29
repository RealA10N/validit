import typing
from .exceptions import (
    InvalidTemplateConfiguration,
    InvalidLengthRange,
)

from .errors import (
    TemplateCheckError,
    TemplateCheckInvalidDataError,
    TemplateCheckMissingDataError,
    TemplateCheckListLengthError,
)

from .error_managers import (
    TemplateCheckErrorManager,
    TemplateCheckErrorCollection as ErrorCollection,
    TemplateCheckRaiseOnError as RaiseOnErrorManager,
)

ErrorManager = typing.TypeVar('ErrorManager', bound=TemplateCheckErrorManager)

classname = lambda instance: type(instance).__name__


class Template:

    def __init__(self, *types: type):
        self.types = types

        for type_ in types:
            if not isinstance(type_, type):
                # If not a basic type like `str`, `int`, etc.
                raise InvalidTemplateConfiguration(
                    "The 'Template' constructor accepts object types, " +
                    f"not '{classname(type_)}'"
                )

    def check(self,
              data: typing.Any,
              path: typing.Tuple[str] = tuple(),
              errors: ErrorManager = ErrorCollection(),
              ) -> ErrorManager:

        if not isinstance(data, self.types):
            # If the given data is not an instance of the allowed types,
            # an error is registered.
            errors.register_error(TemplateCheckInvalidDataError(
                path=path,
                expected=self.types,
                got=data,
            ))

        return errors


class TemplateList(Template):

    def __init__(self, element_template: Template, length: range = None):
        super().__init__(list, tuple)
        self.element_template = element_template
        self.length = length

        if not isinstance(element_template, Template):
            raise InvalidTemplateConfiguration(
                "The 'TemplateList' constructor recives a template instance, " +
                f'not {classname(element_template)}'
            )

        if length is not None and not isinstance(length, range):
            raise InvalidLengthRange(
                "List length should be a 'range' instance, " +
                f"not '{classname(length)}'"
            )

    def check(self,
              data: typing.Any,
              path: typing.Tuple[str] = tuple(),
              errors: ErrorManager = ErrorCollection(),
              ) -> ErrorManager:

        # Check if data is a list
        temp_errors = RaiseOnErrorManager()
        try: super().check(data, path, temp_errors)
        except TemplateCheckError as error:
            # If caught an error, register it!
            errors.register_error(error)

        else:

            if self.length is not None:
                if len(data) not in self.length:
                    errors.register_error(TemplateCheckListLengthError(
                        path=path,
                        expected=self.length,
                        got=len(data),
                    ))

            # For each element in the list,
            # check if it follows the element template
            for index, element in enumerate(data):
                # append current list index to path
                cur_path = path + (str(index),)
                self.element_template.check(element, cur_path, errors)

        return errors


class TemplateDict(Template):

    def __init__(self, **template):
        super().__init__(dict)
        self.template = template

        # Check if all values are template instances
        try: error_element = next(
            element
            for element in template.values()
            if not isinstance(element, Template)
        )

        # If found a non template instance, raises an error
        except StopIteration: pass
        else:
            raise InvalidTemplateConfiguration(
                "Kwargs values should be template instances, " +
                f"not '{classname(error_element)}'"
            )

    def check(self,
              data: typing.Any,
              path: typing.Tuple[str] = tuple(),
              errors: ErrorManager = ErrorCollection(),
              ) -> ErrorManager:

        # Check if the data is a dictionary
        temp_errors = RaiseOnErrorManager()
        try: super().check(data, path, temp_errors)
        except TemplateCheckError as error:
            # If an error found, register it!
            errors.register_error(error)

        else:
            for key in self.template:
                cur_path = path + (key,)
                if key not in data:
                    errors.register_error(
                        TemplateCheckMissingDataError(cur_path))
                else:
                    self.template[key].check(data[key], cur_path, errors)

        return errors
