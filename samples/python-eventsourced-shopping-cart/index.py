"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from akkaserverless.akkaserverless_service import AkkaServerlessService
from api_impl import entity as myapi
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # tag::add-entity[]    
    # create service and add components
    service = AkkaServerlessService()
    service.add_component(myapi)
    # end::add-entity[]
    service.start()
