"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""


# tag::entity-class[]
# imports fom Akka Serverless SDK
from akkaserverless.value_context import ValueEntityCommandContext
from akkaserverless.value_entity import ValueEntity          

from google.protobuf.empty_pb2 import Empty
from counter_api_pb2 import (IncreaseValue, DecreaseValue, ResetValue, GetCounter, CurrentCounter, _COUNTERSERVICE, DESCRIPTOR as API_DESCRIPTOR)
from counter_domain_pb2 import (CounterState)

entity = ValueEntity(_COUNTERSERVICE, [API_DESCRIPTOR], 'counters', init)
# end::entity-class[]

# tag::initial[]
def init(entity_id: str) -> CounterState:
    return CounterState()
# end::initial[]

# tag::increase[]
@entity.command_handler("Increase")
def increase_value(state: CounterState, command: IncreaseValue, context: ValueEntityCommandContext):
    state.value += command.value
    context.update_state(state)
    return Empty()
# end::increase[]

@entity.command_handler("Decrease")
def decrease_value(state: CounterState, command: DecreaseValue, context: ValueEntityCommandContext):
    state.value -= command.value
    context.update_state(state)
    return Empty()

@entity.command_handler("Reset")
def reset_value(state: CounterState, command: ResetValue, context: ValueEntityCommandContext):
    state.value = 0
    context.update_state(state)
    return Empty()

# tag::get-current[]
@entity.command_handler("GetCurrentCounter")
def get_counter(state: CounterState, command: GetCounter, context: ValueEntityCommandContext):
    return CurrentCounter(value=state.value)
# end::get-current[]