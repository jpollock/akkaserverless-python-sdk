Akka Serverless makes development and operation of high-performing stateful services enjoyable: it provides SDKs for building services, and a managed cloud platform for deploying them. The SDKs expose a simple programming model, available in popular programming languages, that eliminates the need for plumbing code to handle database access or connections. The managed platform relieves you from configuring and maintaining the orchestration platform, and the data stores. Akka Serverless auto-scales services, and handles network partitions and failures. It also gives clear visibility into the running system with unified and scalable logging and monitoring.

Read more [here](https://developer.lightbend.com/docs/akka-serverless/index.html) and sign-up [here](https://console.akkaserverless.com/p/register#) for a free account. 

The Akka Serverless Python user language support is a library that implements the Akka Serverless protocol and offers an pythonistic API 
for writing components that implement the types supported by the Akka Serverless protocol. It is a [Tier 3 SDK](https://developer.lightbend.com/docs/akka-serverless/reference/service-api-reference.html).

The Akka Serverless documentation can be found [here](https://developer.lightbend.com/docs/akka-serverless/index.html)

## Install and update using pip:

```
pip install -U akkaserverless
```
## Use Starter App

Visit https://github.com/jpollock/akka-serverless-starter-python to use that repository as a template. Simply click "Use this template". (Explanation for the process, general to Github, is [here](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/creating-a-repository-from-a-template)).


## A Simple EventSourced Example:

### 1. Define your gRPC contract

```
// This is the public API offered by the shopping cart entity.
syntax = "proto3";

import "google/protobuf/empty.proto";
import "akkaserverless/annotations.proto";
import "google/api/annotations.proto";
import "google/api/http.proto";

package com.example.shoppingcart;

message AddLineItem {
    string user_id = 1 [(akkaserverless.field).entity_key = true];
    string product_id = 2;
    string name = 3;
    int32 quantity = 4;
}

message RemoveLineItem {
    string user_id = 1 [(akkaserverless.field).entity_key = true];
    string product_id = 2;
}

message GetShoppingCart {
    string user_id = 1 [(akkaserverless.field).entity_key = true];
}

message LineItem {
    string product_id = 1;
    string name = 2;
    int32 quantity = 3;
}

message Cart {
    repeated LineItem items = 1;
}

service ShoppingCart {
    rpc AddItem(AddLineItem) returns (google.protobuf.Empty) {
        option (google.api.http) = {
            post: "/cart/{user_id}/items/add",
            body: "*",
        };
    }

    rpc RemoveItem(RemoveLineItem) returns (google.protobuf.Empty) {
        option (google.api.http).post = "/cart/{user_id}/items/{product_id}/remove";
    }

    rpc GetCart(GetShoppingCart) returns (Cart) {
        option (google.api.http) = {
          get: "/carts/{user_id}",
          additional_bindings: {
            get: "/carts/{user_id}/items",
            response_body: "items"
          }
        };
    }
}

```

### 2. Generate Python files

It is necessary to compile your .proto files using the protoc compiler in order to generate Python files. 
See [this official gRPC for Python quickstart](https://grpc.io/docs/languages/python/quickstart/) if you are not familiar with the gRPC protocol.

Here is an example of how to compile the sample proto file:
```
python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/shoppingcart.proto
```

### 3. Implement your business logic under an EventSourced Akka Serverless Entity

```
from dataclasses import dataclass, field
from typing import MutableMapping

from google.protobuf.empty_pb2 import Empty

from akkaserverless.event_sourced_context import EventSourcedCommandContext
from akkaserverless.event_sourced_entity import EventSourcedEntity
from shoppingcart.domain_pb2 import (Cart as DomainCart, LineItem as DomainLineItem, ItemAdded, ItemRemoved)
from shoppingcart.shoppingcart_pb2 import (Cart, LineItem, AddLineItem, RemoveLineItem)
from shoppingcart.shoppingcart_pb2 import (_SHOPPINGCART, DESCRIPTOR as FILE_DESCRIPTOR)


@dataclass
class ShoppingCartState:
    entity_id: str
    cart: MutableMapping[str, LineItem] = field(default_factory=dict)


def init(entity_id: str) -> ShoppingCartState:
    return ShoppingCartState(entity_id)


entity = EventSourcedEntity(_SHOPPINGCART, [FILE_DESCRIPTOR], 'carts', init)


def to_domain_line_item(item):
    domain_item = DomainLineItem()
    domain_item.productId = item.product_id
    domain_item.name = item.name
    domain_item.quantity = item.quantity
    return domain_item


@entity.snapshot()
def snapshot(state: ShoppingCartState):
    cart = DomainCart()
    cart.items = [to_domain_line_item(item) for item in state.cart.values()]
    return cart


def to_line_item(domain_item):
    item = LineItem()
    item.product_id = domain_item.productId
    item.name = domain_item.name
    item.quantity = domain_item.quantity
    return item


@entity.snapshot_handler()
def handle_snapshot(state: ShoppingCartState, domain_cart: DomainCart):
    state.cart = {domain_item.productId: to_line_item(domain_item) for domain_item in domain_cart.items}


@entity.event_handler(ItemAdded)
def item_added(state: ShoppingCartState, event: ItemAdded):
    cart = state.cart
    if event.item.productId in cart:
        item = cart[event.item.productId]
        item.quantity = item.quantity + event.item.quantity
    else:
        item = to_line_item(event.item)
        cart[item.product_id] = item


@entity.event_handler(ItemRemoved)
def item_removed(state: ShoppingCartState, event: ItemRemoved):
    del state.cart[event.productId]


@entity.command_handler("GetCart")
def get_cart(state: ShoppingCartState):
    cart = Cart()
    cart.items.extend(state.cart.values())
    return cart


@entity.command_handler("AddItem")
def add_item(item: AddLineItem, ctx: EventSourcedCommandContext):
    if item.quantity <= 0:
        ctx.fail("Cannot add negative quantity of to item {}".format(item.productId))
    else:
        item_added_event = ItemAdded()
        item_added_event.item.CopyFrom(to_domain_line_item(item))
        ctx.emit(item_added_event)
    return Empty()


@entity.command_handler("RemoveItem")
def remove_item(state: ShoppingCartState, item: RemoveLineItem, ctx: EventSourcedCommandContext):
    cart = state.cart
    if item.product_id not in cart:
        ctx.fail("Cannot remove item {} because it is not in the cart.".format(item.productId))
    else:
        item_removed_event = ItemRemoved()
        item_removed_event.productId = item.product_id
        ctx.emit(item_removed_event)
    return Empty()
```

### 4. Register Entity

```
from akkaserverless.akkaserverless_service import AkkaServerlessService
from shoppingcart.shopping_cart_entity import entity as shopping_cart_entity
import logging

if __name__ == '__main__':
    logging.basicConfig()
    service = AkkaServerlessService()
    service.add_component(shopping_cart_entity)
    service.start()

```

### 5. Deployment

See [here](https://developer.lightbend.com/docs/akka-serverless/deploying/index.html) for deployment information.

## Contributing

TODO

## Links

* [Website](https://https://www.lightbend.com/akka-serverless/)
* [Documentation](https://developer.lightbend.com/docs/akka-serverless/)
* [Releases](https://pypi.org/project/akkaserverless/)
* [Code](https://github.com/jpollock/akkaserverless-python-sdk)
* [Issue tracker](https://github.com/jpollock/akkaserverless-python-sdk/issues)
