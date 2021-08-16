"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

import logging

from akkaserverless.akkaserverless import AkkaServerlessService
from akkaserverless.test.actiondemo.action_definition import definition, definition2
from akkaserverless.test.shoppingcart import shopping_cart_entity

logger = logging.getLogger()


def run_test_server(
    run_shopping_cart: bool = True, run_function_demo: bool = True, port: int = 8080
):
    server_builder = AkkaServerlessService().host("0.0.0.0").port(str(port))
    if run_shopping_cart:
        logger.info("adding shoppingcart service")
        server_builder = server_builder.register_event_sourced_entity(
            shopping_cart_entity.entity
        )
    if run_function_demo:
        logger.info("adding ActionDemo service")
        server_builder = server_builder.register_action_entity(definition)
        server_builder = server_builder.register_action_entity(definition2)

    return server_builder.start()
