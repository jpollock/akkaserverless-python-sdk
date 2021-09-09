"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from dataclasses import dataclass, field
from typing import Any, List

from akkaserverless.contexts import ClientActionContext
from akkaserverless.akkaserverless.component.component_pb2 import Forward, SideEffect


@dataclass
class ReplicatedEntityCommandContext(ClientActionContext):
    """An value entity command context.
    Command Handler Methods may take this is a parameter. It allows emitting
    new events in response to a command, along with forwarding the result to other
    entities, and performing side effects on other entities"""

    command_name: str
    command_id: int
    entity_id: str
    sequence: int
    errors: List[str] = field(default_factory=list)
    effects: List[SideEffect] = field(default_factory=list)
    forward: Forward = None
    state = None

    def set_state(self, state):
        """
        Emit the given event. The event will be persisted, and the handler of the
        event defined in the current behavior will immediately be executed to pick it up
        """
        self.state = state

    