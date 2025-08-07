from ..langfuse_config import langfuse_client
from .base_prompt import BasePromptManagement

class LangfusePromptManagement(BasePromptManagement):
    """
    Class for managing Langfuse prompts.
    This class extends the BasePromptManagement to provide Langfuse-specific prompt retrieval.
    """
    
    def __init__(self):
        super().__init__()
        self.langfuse_client = langfuse_client
    
    def get_prompt(self, prompt_name, label = None):
        return self.langfuse_client.get_prompt(prompt_name, label=label).prompt