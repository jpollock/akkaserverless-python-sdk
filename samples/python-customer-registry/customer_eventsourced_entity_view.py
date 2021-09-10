"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""
# tag::register[]

from dataclasses import dataclass, field
from typing import MutableSet

from google.protobuf.empty_pb2 import Empty

from akkaserverless.view import View
from customer_view_eventsourced_pb2 import (_PRODUCTVIEW, DESCRIPTOR as FILE_DESCRIPTOR)

view = View(_PRODUCTVIEW,[FILE_DESCRIPTOR])
# end::register[]


# tag::process-events[]


# end::process-events[]