"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

import logging
from typing import List

import grpc
from google.protobuf import symbol_database as _symbol_database
from grpc._server import _RequestIterator

from akkaserverless.action_context import ActionContext
from akkaserverless.akkaserverless.component.action.action_pb2 import ActionCommand, ActionResponse
from akkaserverless.akkaserverless.component.action.action_pb2_grpc import ActionsServicer
from akkaserverless.action_protocol_entity import Action, ActionHandler
from akkaserverless.akkaserverless.component.component_pb2 import ClientAction
from akkaserverless.utils.payload_utils import get_payload

_sym_db = _symbol_database.Default()

TYPE_URL_PREFIX = "type.googleapis.com/"


class AkkaServerlessActionProtocolServicer(ActionsServicer):
    def __init__(self, action_protocol_entities: List[Action]):
        self.action_protocol_entities = {
            entity.name(): entity for entity in action_protocol_entities
        }
        assert len(action_protocol_entities) == len(self.action_protocol_entities)

    def HandleUnary(self, request: ActionCommand, context):
        logging.info(f"handling unary {request} {context}.")
        if request.service_name in self.action_protocol_entities:
            service = self.action_protocol_entities[request.service_name]
            handler = ActionHandler(service)
            ctx = ActionContext(request.name)
            result = None
            try:
                result = handler.handle_unary(
                    get_payload(request), ctx
                )  # the proto the user defined function returned.
            except Exception as ex:
                ctx.fail(str(ex))
                logging.exception("Failed to execute command:" + str(ex))

            client_action: ClientAction = ctx.create_client_action(result, False)
            action_reply = ActionResponse()

            if not ctx.has_errors():
                action_reply.side_effects.extend(ctx.effects)
                if client_action.HasField("reply"):
                    action_reply.reply.CopyFrom(client_action.reply)
                elif client_action.HasField("forward"):
                    action_reply.forward.CopyFrom(client_action.forward)
            else:
                action_reply.failure.CopyFrom(client_action.failure)
            return action_reply

    def HandleStreamed(self, request_iterator: _RequestIterator, context):
        peek = request_iterator.next()  # evidently, the first message has no payload
        # and is probably intended to prime the stream handler.
        if peek.service_name in self.action_protocol_entities:
            handler = ActionHandler(self.action_protocol_entities[peek.service_name])
            logging.debug(f"set stream handler to {peek.service_name}")
        else:
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details("Method not implemented!")
            raise NotImplementedError("Method not implemented!")

        reconstructed = (get_payload(x) for x in request_iterator)
        ctx = ActionContext(peek.name)
        try:
            result = handler.handle_stream(
                reconstructed, ctx
            )  # the proto the user defined function returned.
            for r in result:
                client_action = ctx.create_client_action(r, False)
                action_reply = ActionResponse()
                if not ctx.has_errors():
                    action_reply.side_effects.extend(ctx.effects)
                    if client_action.HasField("reply"):
                        action_reply.reply.CopyFrom(client_action.reply)
                    elif client_action.HasField("forward"):
                        action_reply.forward.CopyFrom(client_action.forward)
                else:
                    action_reply.failure.CopyFrom(client_action.failure)
                yield action_reply

        except Exception as ex:
            ctx.fail(str(ex))
            logging.exception("Failed to execute command:" + str(ex))

    def HandleStreamedIn(self, request_iterator, context):
        peek = request_iterator.next()  # evidently, the first message has no payload
        # and is probably intended to prime the stream handler.
        logging.debug(f"peeked: {peek}")
        if peek.service_name in self.action_protocol_entities:
            handler = ActionHandler(self.action_protocol_entities[peek.service_name])
            logging.debug(f"set stream in handler to {peek.service_name}")
        else:
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details("Method not implemented!")
            raise NotImplementedError("Method not implemented!")

        reconstructed = (get_payload(x) for x in request_iterator)
        ctx = ActionContext(peek.name)
        try:
            result = handler.handle_stream_in(
                reconstructed, ctx
            )  # the proto the user defined function returned.
            client_action = ctx.create_client_action(result, False)
            action_reply = ActionResponse()
            if not ctx.has_errors():
                action_reply.side_effects.extend(ctx.effects)
                if client_action.HasField("reply"):
                    action_reply.reply.CopyFrom(client_action.reply)
                elif client_action.HasField("forward"):
                    action_reply.forward.CopyFrom(client_action.forward)
            else:
                action_reply.failure.CopyFrom(client_action.failure)
            return action_reply

        except Exception as ex:
            ctx.fail(str(ex))
            logging.exception("Failed to execute command:" + str(ex))

    def HandleStreamedOut(self, request, context):
        if request.service_name in self.action_protocol_entities:
            handler = ActionHandler(self.action_protocol_entities[request.service_name])
        else:
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)
            context.set_details("Method not implemented!")
            raise NotImplementedError("Method not implemented!")

        reconstructed = get_payload(request)
        ctx = ActionContext(request.name)
        try:
            for result in handler.handle_stream_out(reconstructed, ctx):
                client_action = ctx.create_client_action(result, False)
                action_reply = ActionResponse()
                if not ctx.has_errors():
                    action_reply.side_effects.extend(ctx.effects)
                    if client_action.HasField("reply"):
                        action_reply.reply.CopyFrom(client_action.reply)
                    elif client_action.HasField("forward"):
                        action_reply.forward.CopyFrom(client_action.forward)
                else:
                    action_reply.failure.CopyFrom(client_action.failure)
                yield action_reply

        except Exception as ex:
            ctx.fail(str(ex))
            logging.exception("Failed to execute command:" + str(ex))
