"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from akkaserverless.akkaserverless_service import AkkaServerlessService
from product_entity import entity as product_entity
from product_value_entity import entity as product_value_entity
from product_view import view as product_view
from product_view_eventsourced import view as product_view_eventsourced
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    
    service = AkkaServerlessService()
    #service.add_component(product_value_entity)
    #service.add_component(product_view)
    service.add_component(product_entity)
    #service.add_component(product_view_eventsourced)

    service.start()
