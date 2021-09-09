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
from product_api_eventsourced_pb2 import (Product, _GETPRODUCTCOMMAND, _PRODUCTSERVICE, DESCRIPTOR as API_DESCRIPTOR)
#ProductAdded

import statistics


def init(entity_id: str) -> ProductState:
    cs = ProductState()
    cs.name = ""
    return cs


entity = EventSourcedEntity(_PRODUCTSERVICE, [API_DESCRIPTOR, DOMAIN_DESCRIPTOR], 'products', init)

#entity = ValueEntity(_PRODUCTSERVICE, [API_DESCRIPTOR, DOMAIN_DESCRIPTOR], 'products', init)

'''
# Event Sourced
'''

@entity.command_handler("AddProduct")
def add(state: ProductState, command: Product, context: EventSourcedCommandContext):
    context.emit(ProductState(product_id= command.product_id, name=command.name))
    return Empty()

@entity.command_handler("GetProduct")
def get(state: ProductState):
    return state

@entity.event_handler(ProductState)
def added(state: ProductState, event: ProductState ):
    state.product_id = event.product_id
    state.name = event.name
    return state