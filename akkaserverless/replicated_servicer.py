"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

import logging
from pprint import pprint
from typing import List

from google.protobuf import symbol_database as _symbol_database

from akkaserverless.akkaserverless.component.entity.entity_pb2 import Command
from akkaserverless.replicated_context import (
    ReplicatedEntityCommandContext
)
from akkaserverless.replicated_entity import ReplicatedEntity, ReplicatedHandler
from akkaserverless.akkaserverless.component.replicatedentity.replicated_entity_pb2 import (
    ReplicatedEntityStreamIn,
    ReplicatedEntityStreamOut,
    ReplicatedEntityDelta,
    ReplicatedCounterDelta,
    ReplicatedEntityReply,
    ReplicatedEntityStateAction
)
from akkaserverless.akkaserverless.component.replicatedentity.replicated_entity_pb2_grpc import ReplicatedEntitiesServicer
from akkaserverless.utils.payload_utils import get_payload, pack

_sym_db = _symbol_database.Default()

TYPE_URL_PREFIX = "type.googleapis.com/"


class AkkaServerlessReplicatedServicer(ReplicatedEntitiesServicer):
    def __init__(self, replicated_entities: List[ReplicatedEntity]):
        self.replicated_entities = {
            entity.name(): entity for entity in replicated_entities
        }

    def Handle(self, request_iterator, context):
        initiated = False
        current_state = None
        handler: ReplicatedHandler = None
        entity_id: str = None
        start_sequence_number: int = 0
        for request in request_iterator:
            #print(request)
            
            if not initiated:
                if request.HasField("init"):
                    init: ValueInit = request.init
                    service_name = init.service_name
                    entity_id = init.entity_id
                    if service_name not in self.replicated_entities:
                        raise Exception(
                            "No replicated entity registered for service {}".format(
                                service_name
                            )
                        )
                    entity = self.replicated_entities[service_name]
                    handler = ReplicatedHandler(entity)
                    current_state = handler.init_state(entity_id)
                    initiated = True

                else:
                    raise Exception(
                        "Cannot handle {} before initialization".format(request)
                    )

            elif request.HasField("command"):

                command: Command = request.command
                cmd = get_payload(command)
                
                ctx = ReplicatedEntityCommandContext(
                    command.name, command.id, entity_id, start_sequence_number
                )
                result = None
                try:
                    result = handler.handle_command(current_state, cmd, ctx)
                except Exception as ex:
                    ctx.fail(str(ex))
                    logging.exception("Failed to execute command:" + str(ex))

                current_state = result
                #print('dasasdasd')
                #print(type(result))
                #print(result)
                client_action = ctx.create_client_action(result, False)
                
                replicated_reply = ReplicatedEntityReply()
                replicated_reply.command_id = command.id
                replicated_reply.client_action.CopyFrom(client_action)
 
                d = ReplicatedCounterDelta(change=1)

                update = ReplicatedEntityDelta(counter=d)

                state_action = ReplicatedEntityStateAction(update=update)
                replicated_reply.state_action.CopyFrom(state_action)
                replicated_reply.side_effects.extend(ctx.effects)

                output = ReplicatedEntityStreamOut()
                output.reply.CopyFrom(replicated_reply)
                
                yield output

            else:
                raise Exception(
                    "Cannot handle {} after initialization".format(type(request))
                )
            