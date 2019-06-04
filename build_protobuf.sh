#!/bin/bash

python3 -m grpc_tools.protoc --python_out=./game/server/generated --grpc_python_out=game/server/generated --proto_path=./game/server/protobuf progue.proto
