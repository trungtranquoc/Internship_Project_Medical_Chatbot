from abc import ABC, abstractmethod
import inspect
from .state import State

from ..prompt import prompt_management
from ..langfuse_config import create_observed_method
from ..models import open_ai_model

class BaseNode(ABC):
    """
        Centralization of all nodes in the system. Wrapped the graph for observability and tracing in Langfuse.
    """

    def __init__(self, logger):
        self.logger = logger
        self.msgs = []

    def _add_msg(self, msg: tuple[str, str]):
        self.msgs.append(msg)

    def __init_subclass__(cls, **kwargs):
        """
            Override the _call method to automatically wrap it with Langfuse's observation.
        """
        super().__init_subclass__(**kwargs)
        cls.call_params = inspect.signature(cls._call).parameters
        cls._call = create_observed_method(node_name=cls.__name__, original_method=cls._call)

    def _get_prompt(self, prompt_name, label=None):
        return prompt_management.get_prompt(prompt_name, label)
    
    def _invoke(self):
        """
        Invoke the chain with the current prompt and return the response.
        This method can be overridden by subclasses to customize the invocation.
        """
        response = open_ai_model.invoke(self.msgs)
        return response.content
    
    @abstractmethod
    def _call(self, **args):
        """
            Abstract method to be implemented by any Graph Node. Hiearchical structure of nodes allow Langfuse to observe the actual input and output of each node.
        """
        pass

    def __call__(self, state: State):
        # Auto filtering arguments based on the method signature
        filtered_args = {k: v for k, v in state.items() if k in self.call_params}
        self.logger.info(f"Start with params: {filtered_args}")  # Debugging line to see filtered arguments

        return self._call(**filtered_args)

# Test wrapping 
if __name__ == "__main__":
    class SubNode(BaseNode):
        def __init__(self, logger):
            print(f"Init subnode")
            super().__init__(logger, node_name="sub_node")
        
        def _call(self, hello: str):
            return hello

    node = SubNode(logger=None)
    print(node(state={"hello": "Hello"}))