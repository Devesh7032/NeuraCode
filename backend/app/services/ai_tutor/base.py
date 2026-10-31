from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_response(self, system_instruction: str, user_prompt: str, context: Dict[str, Any]) -> str:
        """
        Generates a tutor response given system instructions, user prompt, and sanitized learning context.
        """
        pass
