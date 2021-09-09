"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from dataclasses import dataclass, field
from typing import MutableSet

from google.protobuf.empty_pb2 import Empty

from akkaserverless.replicated_context import ReplicatedEntityCommandContext
from akkaserverless.replicated_entity import ReplicatedEntity
from akkaserverless.replicated.counter import ReplicatedCounter
from akkaserverless.replicated.counter_map import ReplicatedCounterMap
from akkaserverless.replicated.multi_map import ReplicatedMultiMap
from akkaserverless.replicated.vote import ReplicatedVote
from replicated_entity_example_pb2 import (UpdateCounter, CounterValue, _REPLICATEDENTITYEXAMPLE, DESCRIPTOR as API_DESCRIPTOR)

'''
def init(entity_id: str) -> ReplicatedCounter:
    return ReplicatedCounter()

def init(entity_id: str) -> ReplicatedCounterMap:
    return ReplicatedCounterMap()

def init(entity_id: str) -> ReplicatedMultiMap:
    return ReplicatedMultiMap()
'''
def init(entity_id: str) -> ReplicatedVote:
    return ReplicatedVote()


#entity = ReplicatedEntity(_REPLICATEDENTITYEXAMPLE, [API_DESCRIPTOR], ReplicatedCounter, 'counter', init)
#entity = ReplicatedEntity(_REPLICATEDENTITYEXAMPLE, [API_DESCRIPTOR], ReplicatedCounterMap, 'counter', init)
#entity = ReplicatedEntity(_REPLICATEDENTITYEXAMPLE, [API_DESCRIPTOR], ReplicatedMultiMap, 'counter', init)
entity = ReplicatedEntity(_REPLICATEDENTITYEXAMPLE, [API_DESCRIPTOR], ReplicatedVote, 'counter', init)

'''
@entity.command_handler("UpdateReplicatedCounter")
def update(state: ReplicatedCounter, command: UpdateCounter, context: ReplicatedEntityCommandContext):
    context.state.increment(command.value)
    return CounterValue(value=context.state.current_value)


@entity.command_handler("UpdateReplicatedCounter")
def update(state: ReplicatedCounterMap, command: UpdateCounter, context: ReplicatedEntityCommandContext):
    context.state.increment(command.key, command.value)
    return CounterValue(value=context.state.get(command.key).current_value)


@entity.command_handler("UpdateReplicatedCounter")
def update(state: ReplicatedMultiMap, command: UpdateCounter, context: ReplicatedEntityCommandContext):
    context.state.put(command.key, command.value)
    return CounterValue(value=0)
'''        

@entity.command_handler("UpdateReplicatedCounter")
def update(state: ReplicatedVote, command: UpdateCounter, context: ReplicatedEntityCommandContext):
    context.state.vote(True)
    return CounterValue(value=context.state.get_votes())


