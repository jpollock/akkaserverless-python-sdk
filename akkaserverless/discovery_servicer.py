"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

import platform
from dataclasses import dataclass
from logging import getLogger
from pprint import pprint
from typing import List

from google.protobuf.descriptor_pb2 import FileDescriptorProto, FileDescriptorSet
from google.protobuf.descriptor_pool import Default
from google.protobuf.empty_pb2 import Empty

from akkaserverless.akkaserverless.protocol import discovery_pb2
from akkaserverless.action_protocol_entity import Action
from akkaserverless.akkaserverless.protocol.discovery_pb2_grpc import DiscoveryServicer
from akkaserverless.event_sourced_entity import EventSourcedEntity

logger = getLogger()


@dataclass
class AkkaServerlessEntityDiscoveryServicer(DiscoveryServicer):
    #components: List[Component]
    #action_protocol_entities: List[Action]
    event_sourced_entities: List[EventSourcedEntity]
    action_protocol_entities: List[Action]


    def Discover(self, request, context):
        logger.info("discovering.")
        pprint(request)
        descriptor_set = FileDescriptorSet()
        for entity in self.event_sourced_entities + self.action_protocol_entities:
            logger.info(f"entity: {entity.name()}")
            for descriptor in entity.file_descriptors:
                logger.info(f"discovering {descriptor.name}")
                logger.info(f"SD: {entity.service_descriptor.full_name}")
                from_string = FileDescriptorProto.FromString(descriptor.serialized_pb)
                descriptor_set.file.append(from_string)

        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default().FindFileByName("google/protobuf/empty.proto").serialized_pb
            )
        )
        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default().FindFileByName("akkaserverless/eventing.proto").serialized_pb
            )
        )
        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default().FindFileByName("akkaserverless/annotations.proto").serialized_pb
            )
        )
        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default().FindFileByName("akkaserverless/component.proto").serialized_pb
            )
        )
        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default().FindFileByName("akkaserverless/views.proto").serialized_pb
            )
        )
        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default()
                .FindFileByName("google/protobuf/descriptor.proto")
                .serialized_pb
            )
        )
        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default().FindFileByName("google/api/annotations.proto").serialized_pb
            )
        )
        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default().FindFileByName("google/api/http.proto").serialized_pb
            )
        )
        '''
        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default().FindFileByName("google/api/httpbody.proto").serialized_pb
            )
        )
        '''
        descriptor_set.file.append(
            FileDescriptorProto.FromString(
                Default().FindFileByName("google/protobuf/any.proto").serialized_pb
            )
        )
        
        spec = discovery_pb2.Spec(
            service_info=discovery_pb2.ServiceInfo(
                service_name="",
                service_version="0.1.0",
                service_runtime="Python "
                + platform.python_version()
                + " ["
                + platform.python_implementation()
                + " "
                + platform.python_compiler()
                + "]",
                support_library_name="akkaserverless-python-support",
                support_library_version="0.0.1",
            ),
            components=[
                discovery_pb2.Component(
                    component_type=entity.component_type(),
                    service_name=entity.service_descriptor.full_name,
                    entity=discovery_pb2.EntitySettings(entity_type=entity.entity_type)
                )
                for entity in self.event_sourced_entities
                + self.action_protocol_entities
            ],
            proto=descriptor_set.SerializeToString(),
        )
        
        return spec

    def ReportError(self, request, context):
        logger.error(f"Report error: {request}")
        pprint(request)
        return Empty()
