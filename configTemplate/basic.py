import typing
from .exceptions import InvalidTemplateConfiguration

from .errors import (
    TemplateCheckError,
    TemplateCheckInvalidDataError,
    TemplateCheckMissingDataError,
)

from .error_managers import (
    TemplateCheckErrorManager as ErrorManager,
    TemplateCheckErrorCollection as ErrorCollection,
)


class Template:

    def __init__(self, *valid_types: typing.Union[type, 'Template']):
        base_types = list()
        templates = list()

        for type_ in valid_types:
            if isinstance(type_, type):
                # If a basic type like `str`, `int`, etc.
                base_types.append(type_)

            elif isinstance(type_, Template):
                # If an instance of a Template
                templates.append(type_)

            else:
                raise InvalidTemplateConfiguration(
                    "Accepted templates are object types and other template " +
                    f"instances, not '{type(type_).__name__}'"
                )

        # Converting valid type lists to tuples
        self.base_types = tuple(base_types)
        self.templates = tuple(templates)

    def check(self,
              data: typing.Any,
              path: typing.Tuple[str] = tuple(),
              ) -> None:

        # Basic type check
        if isinstance(data, self.base_types):
            # If one of the accepted basic types, accepts it immediately and
            # doesn't raise an error.
            return

        # Template types check
        for template in self.templates:
            try: template.check(data)
            except TemplateCheckError: continue  # If check fails -> tries next template
            else: return  # If check passed successfully -> exits current check

        # If both checks failed, raise an error
        raise TemplateCheckInvalidDataError(
            path=path,
            expected=self.base_types + self.templates,
            got=data,
        )

    def full_check(self,
                   data: typing.Any,
                   path: typing.Tuple[str] = tuple(),
                   errors: ErrorManager = ErrorCollection(),
                   ) -> ErrorManager:
        try: self.check(data, path)
        except TemplateCheckError as error:
            errors.add_error(error)

        return errors


class TemplateList(Template):

    def __init__(self, *valid_types):
        super().__init__(list, tuple)
        self.element_template = Template(*valid_types)

    def check(self,
              data: typing.Any,
              path: typing.Tuple[str] = tuple(),
              ) -> None:
        # Check if data is a list
        super().check(data, path)

        # For each element in the list,
        # check if it follows the element template
        for index, element in enumerate(data):
            # append current list index to path
            cur_path = path + (str(index),)
            self.element_template.check(element, path=cur_path)

    def full_check(self,
                   data: typing.Any,
                   path: typing.Tuple[str] = tuple(),
                   errors: ErrorManager = ErrorCollection(),
                   ) -> ErrorManager:
        try: super().check(data, path)
        except TemplateCheckError as error:
            errors.register_error(error)
        else:
            for index, element in enumerate(data):
                self.element_template.full_check(
                    data=element,
                    path=path + (str(index),),
                    errors=errors
                )

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
                f"not {type(error_element).__name__}"
            )

    def check(self,
              data: typing.Any,
              path: typing.Tuple[str] = tuple(),
              ) -> None:
        # Check if the data is a dictionary
        super().check(data, path)

        # Check if all required keys are present in the given data
        try: missing_key = next(
            key
            for key in self.template
            if key not in data
        )

        # If found missing key, raises `MissingData` error
        except StopIteration: pass
        else:
            missing_path = path + (missing_key,)
            raise TemplateCheckMissingDataError(missing_path)

        # For each key, check for corresponding template
        for key in self.template:
            cur_path = path + (key,)
            self.template[key].check(data[key], path=cur_path)

    def full_check(self,
                   data: typing.Any,
                   path: typing.Tuple[str] = tuple(),
                   errors: ErrorManager = ErrorCollection(),
                   ) -> ErrorManager:
        try: super().check(data, path)
        except TemplateCheckError as error:
            errors.register_error(error)
        else:
            for key in self.template:
                cur_path = path + (key,)
                if key not in data:
                    errors.register_error(
                        TemplateCheckMissingDataError(cur_path))
                else:
                    self.template[key].full_check(
                        data=data[key],
                        path=cur_path,
                        errors=errors,
                    )

        return errors
