from .base_prompt import BasePromptManagement
import yaml
import os

YAML_PATH = "./prompts.yaml"

class YamlPromptManagement(BasePromptManagement):
    """
    Class for managing YAML prompts.
    This class extends the BasePromptManagement to provide YAML-specific prompt retrieval.
    """
    def __init__(self):
        self.prompts = self._load_prompts(YAML_PATH)

    def _load_prompts(self, path: str) -> dict:
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def get_prompt(self, prompt_name: str, label: str = None) -> str:
        """
        Retrieve a YAML prompt by its name and optional label.
        """
        if prompt_name not in self.prompts:
            raise ValueError(f"Prompt '{prompt_name}' not found in YAML file. Please check the YAML file.")
        
        if not label:
            return self.prompts.get(prompt_name, "")
        
        if label not in self.prompts[prompt_name]:
            raise ValueError(f"Label '{label}' not found for prompt '{prompt_name}'. Please check the YAML file.")
        
        return self.prompts.get(prompt_name, {}).get(label, "")