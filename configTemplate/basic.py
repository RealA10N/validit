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
    TemplateCheckErrorManager as ErrorManager,
    TemplateCheckErrorCollection as ErrorCollection,
    TemplateCheckRaiseOnError as RaiseOnErrorManager,
)

classname = lambda instance: type(instance).__name__


class Template:

    def __init__(self, *valid_types: typing.Union[type, 'Template']):
        self.base_types, self.templates = set(), set()

        for type_ in valid_types:
            if isinstance(type_, type):
                # If a basic type like `str`, `int`, etc.
                self.base_types.add(type_)

            elif isinstance(type_, Template):
                # If an instance of a Template
                self.templates.add(type_)

            else:
                raise InvalidTemplateConfiguration(
                    "Accepted templates are object types and other template " +
                    f"instances, not '{classname(type_)}'"
                )

    def check(self,
              data: typing.Any,
              path: typing.Tuple[str] = tuple(),
              errors: ErrorManager = ErrorCollection(),
              ) -> ErrorManager:

        # Basic type check
        if isinstance(data, tuple(self.base_types)):
            # If one of the accepted basic types, accepts it immediately and
            # doesn't raise an error.
            return

        # Template types check
        for template in self.templates:
            try: template.check(data)
            except TemplateCheckError: continue  # If check fails -> tries next template
            else: return  # If check passed successfully -> exits current check

        # If both checks failed, raise an error
        errors.register_error(TemplateCheckInvalidDataError(
            path=path,
            expected=self.base_types | self.templates,
            got=data,
        ))

        return errors


class TemplateList(Template):

    def __init__(self, *valid_types, length: range = None):
        super().__init__(list, tuple)
        self.element_template = Template(*valid_types)

        if length is not None and not isinstance(length, range):
            raise InvalidLengthRange(
                "List length should be a 'range' instance, " +
                f"not '{classname(length)}'"
            )

        self.length = length

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
