"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

import logging
from pprint import pprint
from typing import List

from google.protobuf import symbol_database as _symbol_database

from akkaserverless.akkaserverless.component.entity.entity_pb2 import Command
from akkaserverless.value_context import (
    ValueEntityCommandContext
)
from akkaserverless.value_entity import ValueEntity, ValueHandler
from akkaserverless.akkaserverless.component.valueentity.value_entity_pb2 import (
    ValueEntityInit,
    ValueEntityInitState,
    ValueEntityReply,
    ValueEntityStreamOut,
)
from akkaserverless.akkaserverless.component.valueentity.value_entity_pb2_grpc import ValueEntitiesServicer
from akkaserverless.utils.payload_utils import get_payload, pack

_sym_db = _symbol_database.Default()

TYPE_URL_PREFIX = "type.googleapis.com/"


class AkkaServerlessValueServicer(ValueEntitiesServicer):
    def __init__(self, value_entities: List[ValueEntity]):
        self.value_entities = {
            entity.name(): entity for entity in value_entities
        }

    def Handle(self, request_iterator, context):
        initiated = False
        current_state = None
        handler: ValueHandler = None
        entity_id: str = None
        start_sequence_number: int = 0
        for request in request_iterator:
            if not initiated:
                if request.HasField("init"):
                    init: ValueInit = request.init
                    service_name = init.service_name
                    entity_id = init.entity_id
                    if service_name not in self.value_entities:
                        raise Exception(
                            "No value entity registered for service {}".format(
                                service_name
                            )
                        )
                    entity = self.value_entities[service_name]
                    handler = ValueHandler(entity)
                    current_state = handler.init_state(entity_id)
                    initiated = True
            
                else:
                    raise Exception(
                        "Cannot handle {} before initialization".format(request)
                    )

            elif request.HasField("command"):
                command: Command = request.command
                cmd = get_payload(command)
                ctx = ValueEntityCommandContext(
                    command.name, command.id, entity_id, start_sequence_number, current_state
                )
                result = None
                try:
                    result = handler.handle_command(current_state, cmd, ctx)
                except Exception as ex:
                    ctx.fail(str(ex))
                    logging.exception("Failed to execute command:" + str(ex))

                current_state = ctx.get_state()
                
                client_action = ctx.create_client_action(result, False)
                value_reply = ValueEntityReply()
                value_reply.command_id = command.id
                value_reply.client_action.CopyFrom(client_action)
                value_reply.state_action.CopyFrom(ctx.create_state_action())
                value_reply.side_effects.extend(ctx.effects)

                output = ValueEntityStreamOut()
                output.reply.CopyFrom(value_reply)
                
                yield output

            else:
                raise Exception(
                    "Cannot handle {} after initialization".format(type(request))
                )
