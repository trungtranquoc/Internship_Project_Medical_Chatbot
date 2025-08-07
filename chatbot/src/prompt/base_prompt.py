from abc import ABC, abstractmethod

class BasePromptManagement(ABC):
    """
    Base class for managing prompts in the system.
    This class provides methods to retrieve and invoke prompts.
    """
    
    @abstractmethod
    def get_prompt(self, prompt_name: str, label: str = None) -> str:
        """
        Retrieve a prompt by its name and optional label.
        """
        pass