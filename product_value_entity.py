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
from product_domain_pb2 import (ProductState, DESCRIPTOR as DOMAIN_DESCRIPTOR)
from product_api_pb2 import (Product, Result, _GETPRODUCTCOMMAND, _PRODUCTSERVICE, DESCRIPTOR as API_DESCRIPTOR)


import statistics


def init(entity_id: str) -> ProductState:
    cs = ProductState()
    cs.name = ""
    return cs


#entity = EventSourcedEntity(_CALCULATOR, [FILE_DESCRIPTOR], 'calculators', init)
entity = ValueEntity(_PRODUCTSERVICE, [API_DESCRIPTOR, DOMAIN_DESCRIPTOR], 'products', init)
'''
# Event Sourced
'''
'''
@entity.event_handler(Add)
def added(state: CalculatorState, event: Add):
    state.value += event.amount

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
    value = Value()
    value.amount = state.value
    return value

@entity.command_handler("AddToValue")
def add(item: Add, context: EventSourcedCommandContext):
    
    context.emit(item)
    return Empty()

@entity.command_handler("SubtractFromValue")
def subtract(item: Add, context: EventSourcedCommandContext):
    context.emit(item)
    return Empty()

@entity.command_handler("MultiplyValue")
def multiply(item: Multiply, context: EventSourcedCommandContext):
    context.emit(item)
    return Empty()

@entity.command_handler("DivideValue")
def divide(item: Divide, context: EventSourcedCommandContext):
    context.emit(item)
    return Empty()

'''
@entity.command_handler("AddProduct")
def add(state: ProductState, command: Product, context: ValueEntityCommandContext):
    
    print("FUNCTION: ADD: STATE=")
    print(state)
    state.product_id = command.product_id
    state.name = command.name
    context.update_state(state)
    return Result(text="test")
    
@entity.command_handler("GetProduct")
def get(state: ProductState):
    print("FUNCTION: STATE=")
    print(state)
    return state
