"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, List, MutableMapping

from google.protobuf import descriptor as _descriptor


@dataclass
class View:
    service_descriptor: _descriptor.ServiceDescriptor
    file_descriptors: List[_descriptor.FileDescriptor]

    def component_type(self):
        return "akkaserverless.component.view.Views"

    def name(self):
        return self.service_descriptor.full_name