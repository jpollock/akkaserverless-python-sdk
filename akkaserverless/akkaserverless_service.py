"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""
import logging
import multiprocessing
import os
from concurrent import futures
from dataclasses import dataclass, field
from typing import List, Optional

import grpc

from akkaserverless.akkaserverless.component.action.action_pb2_grpc import add_ActionsServicer_to_server
from akkaserverless.action_protocol_entity import Action
from akkaserverless.action_servicer import AkkaServerlessActionProtocolServicer
from akkaserverless.discovery_servicer import AkkaServerlessEntityDiscoveryServicer
from akkaserverless.akkaserverless.protocol.discovery_pb2_grpc import add_DiscoveryServicer_to_server
from akkaserverless.event_sourced_entity import EventSourcedEntity
from akkaserverless.akkaserverless.component.eventsourcedentity.event_sourced_entity_pb2_grpc import add_EventSourcedEntitiesServicer_to_server
from akkaserverless.eventsourced_servicer import AkkaServerlessEventSourcedServicer

from akkaserverless.view import View
from akkaserverless.value_entity import ValueEntity
from akkaserverless.akkaserverless.component.valueentity.value_entity_pb2_grpc import add_ValueEntitiesServicer_to_server
from akkaserverless.value_servicer import AkkaServerlessValueServicer

# from grpc_reflection.v1alpha import reflection


@dataclass
class AkkaServerlessService:
    logging.basicConfig(
        format="%(asctime)s - %(filename)s - %(levelname)s: %(message)s",
        level=logging.DEBUG,
    )
    logging.root.setLevel(logging.DEBUG)

    __address: str = ""
    __host = "0.0.0.0"
    __port = "8080"
    __workers = multiprocessing.cpu_count()
    __event_sourced_entities: List[EventSourcedEntity] = field(default_factory=list)
    __value_entities: List[ValueEntity] = field(default_factory=list)
    __action_protocol_entities: List[Action] = field(default_factory=list)
    __views: List[View] = field(default_factory=list)

    def host(self, address: str):
        """Set the address of the network Host.
        Default Address is 127.0.0.1.
        """
        self.__host = address
        return self

    def port(self, port: str):
        """Set the address of the network Port.
        Default Port is 8080.
        """
        self.__port = port
        return self

    def max_workers(self, workers: Optional[int] = multiprocessing.cpu_count()):
        """Set the gRPC Server number of Workers.
        Default is equal to the number of CPU Cores in the machine.
        """
        self.__workers = workers
        return self

    def add_component(self, component):
        if isinstance(component, Action):
            self.__action_protocol_entities.append(component)
        elif isinstance(component, EventSourcedEntity):
            self.__event_sourced_entities.append(component)
        elif isinstance(component, ValueEntity):
            self.__value_entities.append(component)
        elif isinstance(component, View):
            self.__views.append(component)
        return self
        

    def start(self):
        """Start the user function and gRPC Server."""

        self.__address = "{}:{}".format(
            os.environ.get("HOST", self.__host), os.environ.get("PORT", self.__port)
        )

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.__workers))

        add_DiscoveryServicer_to_server(
            AkkaServerlessEntityDiscoveryServicer(
                self.__event_sourced_entities, self.__value_entities, self.__views, self.__action_protocol_entities
            ),
            server,
        )
        add_EventSourcedEntitiesServicer_to_server(
            AkkaServerlessEventSourcedServicer(self.__event_sourced_entities), server
        )
        add_ValueEntitiesServicer_to_server(
            AkkaServerlessValueServicer(self.__value_entities), server
        )
        add_ActionsServicer_to_server(
            AkkaServerlessActionProtocolServicer(self.__action_protocol_entities),
            server,
        )
        
        logging.info("Starting Akka Serverless on address %s", self.__address)
        try:
            server.add_insecure_port(self.__address)
            server.start()
            server.wait_for_termination()
        except IOError as e:
            logging.error("Error on start Akka Serverless %s", e.__cause__)
        
        return server

    def ProxyTerminated(self, request, context):
        logger.info(f"Proxy Terminated: {request}")
        return Empty()

    def HealthCheck(self, request, context):
        logger.info(f"Health Check: {request}")
        return Empty()