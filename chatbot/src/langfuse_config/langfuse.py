from langfuse import observe, Langfuse
from langfuse.langchain import CallbackHandler
from opentelemetry.sdk.trace import TracerProvider

import os
from typing import Callable

langfuse_client = Langfuse(
    host=os.environ.get("LANGFUSE_HOST", "https://api.langfuse.com"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    tracer_provider=TracerProvider(),
)

langfuse_callback = CallbackHandler(public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"))


def create_observed_method(node_name: str, original_method: Callable):
    """Create an observed version of the method"""
    def wrapped_method(self, **args):
        @observe(name=node_name)
        def observed_call(**args):              # Passing arguments so that Langfuse can observe the input and output of the function
            return original_method(self, **args)
        return observed_call(**args)
    return wrapped_method