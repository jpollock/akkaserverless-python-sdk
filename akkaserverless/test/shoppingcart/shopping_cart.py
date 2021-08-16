"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from akkaserverless.akkaserverless import AkkaServerlessService
from akkaserverless.test.shoppingcart.shopping_cart_entity import (
    entity as shopping_cart_entity,
)

if __name__ == "__main__":
    AkkaServerlessService().port("8080").register_event_sourced_entity(
        shopping_cart_entity
    ).start()
