"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from akkaserverless.akkaserverless_service import AkkaServerlessService


from customer_value_entity import value_entity as customer_value_entity
from customer_value_entity_view import value_view as customer_value_entity_view

from customer_eventsourced_entity import eventsourced_entity as customer_eventsourced_entity
from customer_eventsourced_entity_view import eventsourced_view as customer_eventsourced_entity_view

from api_impl import entity as myapi
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    # tag::start[]    
    # create service and add components
    # tag::register[]
    service = AkkaServerlessService()
    # end::register[]
    service.add_component(customer_value_entity)
    # tag::register[]
    service.add_component(customer_value_entity_view)
    # end::register[]
    # tag::register-event-sourced[]
    service.add_component(customer_eventsourced_entity)
    service.add_component(customer_eventsourced_entity_view)
    # end::register-event-sourced[]
    service.start()
    # end::start[]    
