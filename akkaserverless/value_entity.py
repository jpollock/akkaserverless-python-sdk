"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, List, MutableMapping

from google.protobuf import descriptor as _descriptor

from akkaserverless.value_context import (
    ValueEntityCommandContext
)


@dataclass
class ValueEntity:
    service_descriptor: _descriptor.ServiceDescriptor
    file_descriptors: List[_descriptor.FileDescriptor]
    entity_type: str
    init_state: Callable[[str], Any]
    persistence_id: str = None
    command_handlers: MutableMapping[str, Callable] = field(default_factory=dict)

    def __post_init__(self):
        if not self.persistence_id:
            self.persistence_id = self.service_descriptor.full_name

    def component_type(self):
        return "akkaserverless.component.valueentity.ValueEntities" #_EVENTSOURCEDINIT.full_name

    def command_handler(self, name: str):
        def register_command_handler(function):
            """
            Register the function to handle commands
            """
            if name in self.command_handlers:
                raise Exception(
                    "Command handler function {} already defined for command {}".format(
                        self.command_handlers[name], name
                    )
                )
            if function.__code__.co_argcount > 3:
                raise Exception(
                    "At most three parameters, the current state, the command and the "
                    "context, should be accepted by the command_handler function"
                )
            self.command_handlers[name] = function
            return function

        return register_command_handler

    def name(self):
        return self.service_descriptor.full_name


def invoke(function, parameters):
    ordered_parameters = []

    t = inspect.signature(function)

    for parameter_definition in inspect.signature(function).parameters.values():
        annotation = parameter_definition.annotation
        if annotation == inspect._empty:
            raise Exception(
                f"Cannot inject parameter {parameter_definition.name} of function "
                f"{function}: Missing type annotation"
            )

        # this assumes parameter names specified in user function
        if parameter_definition.name == 'state':
            if isinstance(parameters[0], annotation):
                ordered_parameters.append(parameters[0])
        elif parameter_definition.name == 'event':
            if isinstance(parameters[1], annotation):
                ordered_parameters.append(parameters[1])
        elif parameter_definition.name == 'command':
            if isinstance(parameters[1], annotation):
                ordered_parameters.append(parameters[1])
        elif parameter_definition.name == 'context':
            if isinstance(parameters[2], annotation):
                ordered_parameters.append(parameters[2])

    # The above is not the right solution likely. But the below was not addressing fact that two 
    # parameters, named differently of course, could be of same type.
    '''
    for parameter_definition in inspect.signature(function).parameters.values():
        annotation = parameter_definition.annotation
        if annotation == inspect._empty:
            raise Exception(
                f"Cannot inject parameter {parameter_definition.name} of function "
                f"{function}: Missing type annotation"
            )
        match_found = False
        for param in parameters:
            if isinstance(param, annotation):
                match_found = True
                if param is not None:
                    ordered_parameters.append(param)
                
        if not match_found:
            raise Exception(
                "Cannot inject parameter {} of function {}: No matching value".format(
                    parameter_definition.name, function
                )
            )
    '''
    return function(*ordered_parameters)

@dataclass
class ValueHandler:
    entity: ValueEntity

    def init_state(self, entity_id: str):
        return self.entity.init_state(entity_id)

    def handle_command(self, current_state, command, ctx: ValueEntityCommandContext):
        if ctx.command_name not in self.entity.command_handlers:
            raise Exception(
                f"Missing command handler function for entity {self.entity.name()} and "
                f"command {ctx.command_name}"
            )
        return invoke(
            self.entity.command_handlers[ctx.command_name],
            [current_state, command, ctx],
        )
