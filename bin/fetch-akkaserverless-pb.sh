#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o pipefail

function fetch() {
  local local=$1
  local tag=$2
  local path=$3
  mkdir -p $(dirname $local)
  curl -o ${local} https://raw.githubusercontent.com/akkaserverlessio/akkaserverless/${tag}${path}
}

tag=$1

# Cloudstate protocol
fetch "akkaserverless/entity.proto" $tag "/protocols/protocol/akkaserverless/entity.proto"

fetch "akkaserverless/event_sourced.proto" $tag "/protocols/protocol/akkaserverless/event_sourced.proto"
fetch "akkaserverless/action.proto" $tag "/protocols/protocol/akkaserverless/action.proto"
fetch "akkaserverless/crdt.proto" $tag "/protocols/protocol/akkaserverless/crdt.proto"

# TCK shopping cart example
fetch "akkaserverless/test/shoppingcart/shoppingcart.proto" $tag "/protocols/example/shoppingcart/shoppingcart.proto"
fetch "akkaserverless/test/shoppingcart/persistence/domain.proto" $tag "/protocols/example/shoppingcart/persistence/domain.proto"

# Cloudstate frontend
fetch "akkaserverless/entity_key.proto" $tag "/protocols/frontend/akkaserverless/entity_key.proto"
fetch "akkaserverless/eventing.proto" $tag  "/protocols/frontend/akkaserverless/eventing.proto"

# dependencies
fetch "protobuf/lib/google/api/annotations.proto" $tag "/protocols/frontend/google/api/annotations.proto"
fetch "protobuf/lib/google/api/http.proto" $tag "/protocols/frontend/google/api/http.proto"
fetch "protobuf/lib/google/api/httpbody.proto" $tag "/protocols/frontend/google/api/httpbody.proto"