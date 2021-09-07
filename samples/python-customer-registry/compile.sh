#!/bin/bash

# Prepare script for the akkaserverless-javascript-sdk package

# Delete and recreate the proto directory
rm -rf ./proto
mkdir -p ./proto

# get the framework version from settings.js
readonly framework_version="0.7.0-beta.17"

function download_protocol {
  local module="$1"
  curl -OL "https://repo1.maven.org/maven2/com/akkaserverless/akkaserverless-$module-protocol/$framework_version/akkaserverless-$module-protocol-$framework_version.zip"
  unzip "akkaserverless-$module-protocol-$framework_version.zip"
  cp -r "akkaserverless-$module-protocol-$framework_version"/* proto
  rm -rf "akkaserverless-$module-protocol-$framework_version.zip" "akkaserverless-$module-protocol-$framework_version"
}

# Download and unzip the proxy and SDK protocols to the proto directory
download_protocol sdk
download_protocol proxy

# Compile protobuf
#./scripts/compile-protobuf.sh


for file in *_pb2*; do rm "$file"; done

for file in *.proto; do python -m grpc_tools.protoc --proto_path=./proto  --proto_path=. --python_out=. --grpc_python_out=.  --descriptor_set_out=user-function.desc $file; done

for file in *_pb2*; do perl -i -pe 's/from akkaserverless/from akkaserverless.akkaserverless/g' $file; done
