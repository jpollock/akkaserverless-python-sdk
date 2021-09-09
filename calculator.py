"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from akkaserverless.akkaserverless_service import AkkaServerlessService
from calculator_entity import entity as calculator_entity
from calculator_value_entity import entity as calculator_value_entity
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    AkkaServerlessService().register_event_sourced_entity(calculator_entity).start()
    #AkkaServerlessService().register_value_entity(calculator_value_entity).start()