import os
from ..logger import CustomLogger

from .yaml_prompt import YamlPromptManagement
from .langfuse_prompt import LangfusePromptManagement

LANGFUSE_AVAILABLE = os.getenv("LANGFUSE_AVAILABLE", "False") != "False"
logger = CustomLogger('prompt_management')

logger.info("Loading prompt management system...")
if LANGFUSE_AVAILABLE:
    prompt_management = LangfusePromptManagement()
else:
    prompt_management = YamlPromptManagement()

__all__ = [
    "prompt_management"
]