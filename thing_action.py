"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from dataclasses import dataclass, field
from typing import MutableSet

from google.protobuf.empty_pb2 import Empty

from akkaserverless.action_context import ActionContext
from akkaserverless.action_protocol_entity import Action
from thing_api_action_pb2 import (MyRequest, MyResponse, _THINGACTIONSERVICE, DESCRIPTOR as API_DESCRIPTOR)


action = Action(_THINGACTIONSERVICE, [API_DESCRIPTOR])

@action.unary_handler("Hello")
def hello(command: MyRequest, context: ActionContext):
    resp = MyResponse(text= "Do you want to play a game, " + command.name + "?")
    return resp