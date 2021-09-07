"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

# imports fom Akka Serverless SDK
from akkaserverless.value_context import ValueEntityCommandContext
from akkaserverless.value_entity import ValueEntity          

from google.protobuf.empty_pb2 import Empty
from shoppingcart_api_pb2 import (GetShoppingCart, Cart, AddLineItem, RemoveLineItem,RemoveShoppingCart, _SHOPPINGCARTSERVICE, DESCRIPTOR as API_DESCRIPTOR)
from shoppingcart_domain_pb2 import (LineItem)

def init(entity_id: str) -> Cart:
    return Cart()

entity = ValueEntity(_SHOPPINGCARTSERVICE, [API_DESCRIPTOR], 'carts', init)

@entity.command_handler("AddItem")
def add_item(state: Cart, command: AddLineItem, context: ValueEntityCommandContext):
    state.items.append(LineItem(product_id=command.product_id, name=command.name, quantity=command.quantity))
    context.update_state(state)
    return Empty()


@entity.command_handler("RemoveItem")
def remove_item(state: Cart, command: RemoveLineItem, context: ValueEntityCommandContext):
    state = command
    context.update_state(state)
    return Empty()

@entity.command_handler("GetCart")
def get_cart(state: Cart, command: GetShoppingCart, context: ValueEntityCommandContext):
    return state

@entity.command_handler("RemoveCart")
def remove_cart(state: Cart, command: RemoveShoppingCart, context: ValueEntityCommandContext):
    return Empty()