from .generated import *

import grpc
import logging
import time
from typing import List, Optional, Union, Generator, AsyncGenerator
from .generated import chat_pb2, chat_pb2_grpc
from .config import (
    GRPC_HOST, GRPC_PORT, CONNECTION_TIMEOUT, 
    MAX_RETRY_ATTEMPTS, RETRY_DELAY, MAX_HISTORY_SIZE,
    LOG_LEVEL, LOG_FORMAT
)

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class ChatbotGRPCClient:
    """
    gRPC client for connecting to the chatbot server on port 50051
    """
    
    def __init__(self, host: str = GRPC_HOST, port: int = GRPC_PORT):
        """
        Initialize the gRPC client
        
        Args:
            host (str): Server host address
            port (int): Server port number
        """
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
        self.max_retry_attempts = MAX_RETRY_ATTEMPTS
        self.retry_delay = RETRY_DELAY
        self.connection_timeout = CONNECTION_TIMEOUT
        
    def connect(self) -> bool:
        """
        Establish connection to the gRPC server with retry logic
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        for attempt in range(1, self.max_retry_attempts + 1):
            try:
                logger.info(f"Attempting to connect to gRPC server at {self.host}:{self.port} (attempt {attempt}/{self.max_retry_attempts})")
                
                # Create a gRPC channel
                self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
                
                # Create a stub (client)
                self.stub = chat_pb2_grpc.ChatStub(self.channel)
                
                # Test connection with a simple call
                grpc.channel_ready_future(self.channel).result(timeout=self.connection_timeout)
                logger.info(f"Successfully connected to gRPC server at {self.host}:{self.port}")
                return True
                
            except grpc.RpcError as e:
                logger.warning(f"Attempt {attempt} failed: gRPC error - {e}")
                self._cleanup_connection()
                
            except Exception as e:
                logger.warning(f"Attempt {attempt} failed: {e}")
                self._cleanup_connection()
            
            # Wait before retrying (except for the last attempt)
            if attempt < self.max_retry_attempts:
                logger.info(f"Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)
        
        logger.error(f"Failed to connect to gRPC server after {self.max_retry_attempts} attempts")
        return False
    
    def _cleanup_connection(self):
        """Clean up connection resources"""
        if self.channel:
            self.channel.close()
            self.channel = None
        self.stub = None
    
    def disconnect(self) -> bool:
        """
        Close the gRPC connection
        """
        self._cleanup_connection()
        logger.info("gRPC connection closed")
        return True

    async def send_question(self, query: str, history: Optional[list] = None) -> AsyncGenerator[str, None]:
        """
        Send a question to the chatbot server
        
        Args:
            query (str): The user's question
            history (List[str], optional): Previous conversation history
            
        Returns:
            Optional[str]: The chatbot's response or None if error
        """
        if not self.stub:
            logger.error("gRPC client not connected. Call connect() first.")
            yield None
        
        try:
            # Create request
            request = chat_pb2.QuestionRequest(
                query=query,
                history=history or [],
                isStreaming=True
            )
            
            for resp in self.stub.Answer(request, timeout=60.0):
                # yield partial chunk to caller
                yield resp.answer
            
        except grpc.RpcError as e:
            logger.error(f"gRPC call failed: {e.code()}: {e.details()}")
            yield None
        except Exception as e:
            logger.error(f"Unexpected error during gRPC call: {e}")
            yield None

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()