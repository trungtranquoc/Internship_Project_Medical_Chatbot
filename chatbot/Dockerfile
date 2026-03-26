FROM python:3.11

WORKDIR /code

# 1. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy source code and gRPC definitions
COPY ./src /code/src
COPY ./grpc_generated/chat.proto /code/grpc_generated/chat.proto
COPY server.py /code/server.py
COPY prompts.yaml /code/prompts.yaml

# 3. Create __init__.py for the grpc_generated module
RUN touch /code/grpc_generated/__init__.py

# 4. Generate gRPC Python files
RUN python -m grpc_tools.protoc \
    --python_out=/code/grpc_generated \
    --grpc_python_out=/code/grpc_generated \
    --proto_path=/code/grpc_generated \
    chat.proto

# 5. Fix import paths in generated gRPC files
RUN sed -i 's/import chat_pb2 as chat__pb2/from . import chat_pb2 as chat__pb2/' /code/grpc_generated/chat_pb2_grpc.py

# 6. Expose the gRPC port
EXPOSE 50051

# 7. REMOVED: ENV ENV=production and COPY .env.production
# We now rely entirely on Kubernetes ConfigMaps and Secrets.

CMD ["python", "server.py"]