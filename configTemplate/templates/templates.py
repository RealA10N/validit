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

    def validate(self,
                 container: BaseContainer,
                 errors: ErrorManager,
                 ) -> None:

        if container.data is DefaultValue:
            errors.register_error(
                TemplateCheckMissingDataError(container.path)
            )

        elif not isinstance(container.data, self.types):
            # If the given data is not an instance of the allowed types,
            # an error is registered.
            errors.register_error(TemplateCheckInvalidDataError(
                path=container.path,
                expected=self.types,
                got=container.data,
            ))


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

    def validate(self,
                 container: BaseContainer,
                 errors: ErrorManager,
                 ) -> None:
        if container.data is not DefaultValue:
            # Only preforms the check if the data is provided.
            # if data is not given (data=Default), skips the check!
            self.__template.validate(container, errors)


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

        if (not hasattr(valid_lengths, '__contains__')
                ) or isinstance(valid_lengths, type):
            raise InvalidTemplateConfiguration(
                f"'{valid_lengths}' is not a valid set of list lengths"
            )

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

    def validate(self,
                 container: BaseContainer,
                 errors: ErrorManager,
                 ) -> None:

        # Check if data is a list
        try: super().validate(container, RaiseOnErrorManager())
        except TemplateCheckError as error:
            # If caught an error, register it!
            errors.register_error(error)

        else:

            if len(container.data) not in self.length:
                errors.register_error(TemplateCheckListLengthError(
                    path=container.path,
                    expected=self.length,
                    got=len(container.data),
                ))

            # For each element in the list,
            # check if it follows the element template
            for cur in container:
                self.template.validate(
                    container=cur,
                    errors=errors,
                )


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

    def validate(self,
                 container: BaseContainer,
                 errors: ErrorManager,
                 ) -> None:

        # Check if the data is a dictionary
        try: super().validate(container, RaiseOnErrorManager())
        except TemplateCheckError as error:
            # If an error found, register it!
            errors.register_error(error)

        else:
            for key, template in self.template.items():
                template.validate(
                    container=container[key],
                    errors=errors,
                )
