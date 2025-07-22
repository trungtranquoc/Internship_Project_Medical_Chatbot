
# This script generates gRPC Python code from the chat.proto file.
python -m grpc_tools.protoc \
    --python_out=gRPC/generated/ \
    --grpc_python_out=gRPC/generated/ \
    --proto_path=gRPC/generated/ \
    gRPC/generated/chat.proto

# Adjust imports in the generated files to match the package structure
sed -i '' 's/import chat_pb2 as chat__pb2/from . import chat_pb2 as chat__pb2/' gRPC/generated/chat_pb2_grpc.py