import typing

from collections import defaultdict

from configTemplate.error_managers import (
    TemplateCheckErrorCollection as ErrorCollection,
    TemplateCheckRaiseOnError as RaiseOnErrorManager,
)

from configTemplate.errors import (
    TemplateCheckError,
    TemplateCheckInvalidDataError,
    TemplateCheckMissingDataError,
    TemplateCheckListLengthError,
)

from .base import (
    BaseTemplate,
    DefaultValue,
    ErrorManager,
)

from configTemplate.containers import (
    BaseContainer,
    HeadContainer,
    Container,
)

from configTemplate.exceptions import InvalidTemplateConfiguration
from configTemplate.utils import AnyLength, DefaultValue
from .base import BaseTemplate

classname = lambda instance: type(instance).__name__


class Template(BaseTemplate):

    def __init__(self, *types: type):
        self.types = types

        for type_ in types:
            if not isinstance(type_, type):
                # If not a basic type like `str`, `int`, etc.
                raise InvalidTemplateConfiguration(
                    f"The '{classname(self)}' constructor accepts object types, " +
                    f"not '{classname(type_)}'"
                )

    def container_dump(self,
                       container: BaseContainer,
                       data: typing.Any = DefaultValue,
                       ) -> None:
        if data is not DefaultValue:
            container.data = data

    def check(self,
              data: typing.Any = DefaultValue,
              path: typing.Tuple[str] = tuple(),
              errors: ErrorManager = ErrorCollection(),
              ) -> ErrorManager:

        if data is DefaultValue:
            errors.register_error(TemplateCheckMissingDataError(path))

        elif not isinstance(data, self.types):
            # If the given data is not an instance of the allowed types,
            # an error is registered.
            errors.register_error(TemplateCheckInvalidDataError(
                path=path,
                expected=self.types,
                got=data,
            ))

        return errors


class Optional(BaseTemplate):

    def __init__(self,
                 template: Template,
                 default: typing.Any = DefaultValue
                 ) -> None:
        self.__template = template
        self.__default = default

        if not isinstance(template, Template):
            raise InvalidTemplateConfiguration(
                f"The '{classname(self)}' constructor accepts a 'Template' instance, " +
                f"not '{classname(template)}'"
            )

    def container_dump(self,
                       container: BaseContainer,
                       data: typing.Any = DefaultValue,
                       ) -> None:
        if data is DefaultValue:
            data = self.__default
        if data is not DefaultValue:
            container.data = data

    def check(self,
              data: typing.Any = DefaultValue,
              path: typing.Tuple[str] = tuple(),
              errors: ErrorManager = ErrorCollection(),
              ) -> ErrorManager:
        if data is not DefaultValue:
            # Only preforms the check if the data is provided.
            # if data is not given (data=None), skips the check!
            self.__template.check(data, path, errors)

        return errors


class TemplateList(Template):

    def __init__(self, template: Template, valid_lengths: typing.Any = AnyLength()):
        super().__init__(list, tuple)
        self.template = template
        self.length = valid_lengths

        if not isinstance(template, Template):
            raise InvalidTemplateConfiguration(
                f"The '{classname(self)}' constructor recives a template instance, " +
                f'not {classname(template)}'
            )

        try: _ = 0 in valid_lengths
        except TypeError as error:
            raise InvalidTemplateConfiguration(
                f"'{valid_lengths}' is not a valid set of list lengths"
            ) from error

    def container_dump(self,
                       container: BaseContainer,
                       data: typing.Any = DefaultValue,
                       ) -> None:
        container.data = list()

        if not isinstance(data, (list, tuple)):
            # If data is not a list (maybe default value)
            # contanier will remain with an empty list.
            return

        for index, element in enumerate(data):

            # Increase container length by one
            container.data.append(None)

            # Dump the rest of the data with the element template
            self.template.container_dump(
                container=container[index],
                data=element
            )

    def check(self,
              data: typing.Any = DefaultValue,
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
                self.template.check(element, cur_path, errors)

        return errors


class TemplateDict(Template):

    def __init__(self, **template):
        super().__init__(dict)
        self.template = template

        # Check if all values are template instances
        try: error_element = next(
            element
            for element in template.values()
            if not isinstance(element, BaseTemplate)
        )

        # If found a non template instance, raises an error
        except StopIteration: pass
        else:
            raise InvalidTemplateConfiguration(
                "Kwargs values should be template instances, " +
                f"not '{classname(error_element)}'"
            )

    def container_dump(self,
                       container: BaseContainer,
                       data: typing.Any = DefaultValue,
                       ) -> None:
        container.data = dict()

        if not isinstance(data, dict):
            # If data is not a dict (maybe default value)
            # converts the data into a dict where values for every
            # key is 'DefaultValue'. This is useful and used for
            # dumping optional default data to the container, for example.
            data = defaultdict(lambda _: DefaultValue)

        for key, template in self.template.items():
            template.container_dump(
                container=container[key],
                data=data.get(key, DefaultValue)
            )

    def check(self,
              data: typing.Any = DefaultValue,
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
            for key, template in self.template.items():
                cur_path = path + (key,)
                cur_data = data.get(key, DefaultValue)
                template.check(cur_data, cur_path, errors)

        return errors
