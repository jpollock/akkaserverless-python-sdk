"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from akkaserverless.akkaserverless_service import AkkaServerlessService
from replicated import entity as replicated_entity
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    
    
    service = AkkaServerlessService()
    service.add_component(replicated_entity)

    service.start()
