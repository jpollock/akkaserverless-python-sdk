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
    EventContext,
    ValueCommandContext,
    SnapshotContext,
)
from akkaserverless.value_entity import ValueEntity, ValueHandler
from akkaserverless.value_entity import ValueEntity, ValueHandler
from akkaserverless.akkaserverless.component.valueentity.value_entity_pb2 import (
    ValueEvent,
    ValueInit,
    ValueReply,
    ValueSnapshot,
    ValueStreamOut,
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
                            "No event sourced entity registered for service {}".format(
                                service_name
                            )
                        )
                    entity = self.value_entities[service_name]
                    handler = ValueHandler(entity)
                    current_state = handler.init_state(entity_id)
                    initiated = True
                    if init.HasField("snapshot"):
                        value_snapshot: ValueSnapshot = init.snapshot
                        start_sequence_number = value_snapshot.snapshot_sequence
                        snapshot = get_payload(value_snapshot.snapshot)
                        snapshot_context = SnapshotContext(
                            entity_id, start_sequence_number
                        )
                        snapshot_result = handler.handle_snapshot(
                            current_state, snapshot, snapshot_context
                        )
                        if snapshot_result:
                            current_state = snapshot_result
                else:
                    raise Exception(
                        "Cannot handle {} before initialization".format(request)
                    )

            elif request.HasField("event"):
                event: ValueEvent = request.event
                evt = get_payload(event)
                event_result = handler.handle_event(
                    current_state, evt, EventContext(entity_id, event.sequence)
                )
                start_sequence_number = event.sequence
                if event_result:
                    current_state = event_result
                pprint("Handling event {}".format(event))
            elif request.HasField("command"):
                command: Command = request.command
                cmd = get_payload(command)
                ctx = ValueCommandContext(
                    command.name, command.id, entity_id, start_sequence_number
                )
                result = None
                try:
                    result = handler.handle_command(current_state, cmd, ctx)
                except Exception as ex:
                    ctx.fail(str(ex))
                    logging.exception("Failed to execute command:" + str(ex))

                client_action = ctx.create_client_action(result, False)
                value_reply = ValueReply()
                value_reply.command_id = command.id
                value_reply.client_action.CopyFrom(client_action)
                snapshot = None
                perform_snapshot = False
                if not ctx.has_errors():
                    for number, event in enumerate(ctx.events):
                        sequence_number = start_sequence_number + number + 1
                        event_result = handler.handle_event(
                            current_state,
                            event,
                            EventContext(entity_id, start_sequence_number + number),
                        )
                        if event_result:
                            current_state = event_result
                        snapshot_every = handler.entity.snapshot_every
                        perform_snapshot = (snapshot_every > 0) and (
                            perform_snapshot or (sequence_number % snapshot_every == 0)
                        )
                    end_sequence_number = start_sequence_number + len(ctx.events)
                    if perform_snapshot:
                        snapshot = handler.snapshot(
                            current_state,
                            SnapshotContext(entity_id, end_sequence_number),
                        )

                    value_reply.side_effects.extend(ctx.effects)
                    value_reply.events.extend(
                        [pack(event) for event in ctx.events]
                    )
                    if snapshot:
                        value_reply.snapshot.Pack(snapshot)

                output = ValueStreamOut()
                output.reply.CopyFrom(value_reply)
                yield output

            else:
                raise Exception(
                    "Cannot handle {} after initialization".format(type(request))
                )
