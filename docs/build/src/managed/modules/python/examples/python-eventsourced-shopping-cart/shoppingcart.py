"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""
# tag::lookup-type[]
# import from generated GRPC file(s)
from shoppingcart_api_pb2 import (GetShoppingCart, Cart, AddLineItem, _SHOPPINGCARTSERVICE, DESCRIPTOR as API_DESCRIPTOR)
from shoppingcart_domain_pb2 import (ItemAdded, LineItem)
# end::lookup-type[]

# tag::entity-class[]
# imports fom Akka Serverless SDK
from akkaserverless.event_sourced_context import EventSourcedCommandContext
from akkaserverless.event_sourced_entity import EventSourcedEntity

entity = EventSourcedEntity(_SHOPPINGCARTSERVICE, [API_DESCRIPTOR], 'carts', init)
# end::entity-class[]


# tag::initial[]
def init(entity_id: str) -> Cart:
    return Cart()
# end::initial[]

# tag::add-item[]
# tag::behavior[]
@entity.command_handler("AddItem")
# end::behavior[]
def add(state: Cart, command: AddLineItem, context: EventSourcedCommandContext):
    context.emit(ItemAdded(LineItem(productId= command.product_id, name=command.name)))
    return Empty()
# end::add-item[]

# tag::get-cart[]
@entity.command_handler("GetCart")
def get(state: Cart, command: GetShoppingCart):
    return state
# end::get-cart[]

# tag::item-added[]
@entity.event_handler(Cart)
def added(state: Cart, event: ItemAdded ):
    state.product_id = event.product_id
    state.name = event.name
    return state
# end::item-added[]    