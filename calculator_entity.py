"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from dataclasses import dataclass, field
from typing import MutableSet

from google.protobuf.empty_pb2 import Empty

from akkaserverless.event_sourced_context import EventSourcedCommandContext
from akkaserverless.event_sourced_entity import EventSourcedEntity
from akkaserverless.value_context import ValueEntityCommandContext
from akkaserverless.value_entity import ValueEntity
from Calculator_pb2 import (CalculatorState, Value, Add, Subtract, Multiply, Divide)
from Calculator_pb2 import (_CALCULATOR, DESCRIPTOR as FILE_DESCRIPTOR)

import statistics


def init(entityId: str) -> CalculatorState:
    print(entityId)
    cs = CalculatorState()
    cs.value = 0
    print(cs)
    #cs.history = []
    
    return cs


entity = EventSourcedEntity(_CALCULATOR, [FILE_DESCRIPTOR], 'calculators', init)
#entity = ValueEntity(_CALCULATOR, [FILE_DESCRIPTOR], 'calculators', init)
'''
# Event Sourced
'''

@entity.event_handler(Add)
def added(state: CalculatorState, event: Add):
    state.value += event.amount
    print(state)

@entity.event_handler(Subtract)
def removed(state: CalculatorState, event: Subtract):
    state.value -= event.amount

@entity.event_handler(Multiply)
def multiplied(state: CalculatorState, event: Multiply):
    state.value = state.value * event.amount

@entity.event_handler(Divide)
def divided(state: CalculatorState, event: Divide):
    state.value = int(state.value / event.amount)

@entity.command_handler("GetCurrentValue")
def get_calculator(state: CalculatorState):
    print(state)
    value = Value()
    value.amount = state.value
    return value

@entity.command_handler("AddToValue")
def add(item: Add, ctx: EventSourcedCommandContext):
    
    ctx.emit(item)
    return Empty()

@entity.command_handler("SubtractFromValue")
def subtract(item: Add, ctx: EventSourcedCommandContext):
    ctx.emit(item)
    return Empty()

@entity.command_handler("MultiplyValue")
def multiply(item: Multiply, ctx: EventSourcedCommandContext):
    ctx.emit(item)
    return Empty()

@entity.command_handler("DivideValue")
def divide(item: Divide, ctx: EventSourcedCommandContext):
    ctx.emit(item)
    return Empty()

