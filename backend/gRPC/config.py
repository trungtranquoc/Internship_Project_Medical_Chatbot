"""
Configuration settings for gRPC connection
"""

import os

# gRPC Server Configuration
GRPC_HOST = os.getenv("GRPC_HOST", "localhost")
GRPC_PORT = int(os.getenv("GRPC_PORT", "50051"))

# Connection Settings
CONNECTION_TIMEOUT = int(os.getenv("CONNECTION_TIMEOUT", "5"))  # seconds
MAX_RETRY_ATTEMPTS = int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
RETRY_DELAY = float(os.getenv("RETRY_DELAY", "1.0"))  # seconds

# Conversation History Settings
MAX_HISTORY_SIZE = int(os.getenv("MAX_HISTORY_SIZE", "20"))  # number of messages

# Logging Settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
