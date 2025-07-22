FROM python:3.11

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /code/src
COPY ./grpc_generated/chat.proto /code/grpc_generated/chat.proto
COPY server.py /code/server.py
COPY .env.production /code/.env.production

# Create __init__.py file for grpc_generated module
RUN touch /code/grpc_generated/__init__.py

# Generate gRPC Python files from .proto file
RUN python -m grpc_tools.protoc \
    --python_out=/code/grpc_generated \
    --grpc_python_out=/code/grpc_generated \
    --proto_path=/code/grpc_generated \
    chat.proto

# Fix import paths in generated gRPC files
RUN sed -i 's/import chat_pb2 as chat__pb2/from . import chat_pb2 as chat__pb2/' /code/grpc_generated/chat_pb2_grpc.py

EXPOSE 50051
ENV ENV=production

CMD ["python", "server.py"]