import typing

from copy import deepcopy

from validit.errors.managers import (
    TemplateCheckErrorManager as ErrorManager,
    TemplateCheckErrorCollection as ErrorCollection,
    TemplateCheckRaiseOnError as RaiseOnErrorManager,
)

from validit.errors import (
    TemplateCheckError,
    TemplateCheckInvalidOptionError,
    TemplateCheckInvalidDataError,
    TemplateCheckMissingDataError,
    TemplateCheckListLengthError,
)

from .base import BaseTemplate

from validit.containers import (
    BaseContainer,
    HeadContainer,
)

from validit.exceptions import InvalidTemplateConfiguration, InvalidDefaultValue
from validit.utils import AnyLength, DefaultValue


def classname(instance):
    return type(instance).__name__


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
                TemplateCheckMissingDataError(container)
            )

        elif not isinstance(container.data, self.types):
            # If the given data is not an instance of the allowed types,
            # an error is registered.
            errors.register_error(TemplateCheckInvalidDataError(
                container=container,
                expected=self.types,
                got=container.data,
            ))


class TemplateAny(Template):

    def __init__(self,):
        super().__init__(object)

    def container_dump(self,
                       container: BaseContainer,
                       data=DefaultValue) -> None:
        container.data = deepcopy(data)


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

        # If default value is provided, checks if the default value
        # matches the template
        if default is not DefaultValue:
            try:
                self.__template.validate(
                    container=HeadContainer(default),
                    errors=RaiseOnErrorManager(),
                )

            except TemplateCheckError as error:
                raise InvalidDefaultValue(
                    f"'{classname(self)}' received a default value that doesn't match the template: " +
                    error.no_color_str
                ) from None

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
                f"{valid_lengths!r} is not a valid set of list lengths"
            )

    def container_dump(self,
                       container: BaseContainer,
                       data: typing.Any = DefaultValue,
                       ) -> None:

        if not isinstance(data, (list, tuple)):
            # If data is not a list (maybe default value)
            # contanier will remain with default value.
            container.data = data
            return

        container.data = list()
        for index, element in enumerate(data):

            # Increase container length by one
            container.data.append(DefaultValue)

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
        temp_errors = ErrorCollection()
        super().validate(container, temp_errors)

        if temp_errors:
            temp_errors.dump_errors(errors)

        else:
            if len(container.data) not in self.length:
                errors.register_error(TemplateCheckListLengthError(
                    container=container,
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

        if not isinstance(data, dict):
            # If data is not a dict (maybe default value)
            # contanier will remain with default value.
            container.data = data
            return

        container.data = dict()
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
        temp_errors = ErrorCollection()
        super().validate(container, temp_errors)

        if temp_errors:
            temp_errors.dump_errors(errors)

        else:
            # If no errors in super validation check, run actual validation
            for key, template in self.template.items():
                template.validate(
                    container=container[key],
                    errors=errors,
                )


class Options(BaseTemplate):
    """ This template recives INSTANCES of objects (and not types), and when
    validating, checks for EQUALITY between the data and the given instance.
    This is useful in some cases where the options are pre-defined and limited.

    For example: `Options('L', 'R')` to allow the data to only be strings that
    represent directions. """

    def __init__(self, *instances: typing.Any):
        self.instances = instances

    def container_dump(self,
                       container: BaseContainer,
                       data: typing.Any = DefaultValue,
                       ) -> None:
        container.data = data

    def validate(self,
                 container: BaseContainer,
                 errors: ErrorManager,
                 ) -> None:
        for cur in self.instances:
            if cur is container.data:
                return

        errors.register_error(TemplateCheckInvalidOptionError(
            container=container,
            expected=self.instances,
            got=container.data,
        ))
