import json
from typing import Dict, Any
from app.core.config import settings
from app.services.ai_tutor.base import BaseAIProvider
from app.services.ai_tutor.fallback_provider import FallbackProvider

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        self.fallback = FallbackProvider()

    async def generate_response(self, system_instruction: str, user_prompt: str, context: Dict[str, Any]) -> str:
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            # Fallback when API key is unconfigured
            return await self.fallback.generate_response(system_instruction, user_prompt, context)

        try:
            import urllib.request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            
            prompt_content = f"{system_instruction}\n\nContext:\n{json.dumps(context, indent=2)}\n\nUser Question:\n{user_prompt}"
            body = {
                "contents": [
                    {
                        "parts": [{"text": prompt_content}]
                    }
                ]
            }

            req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")

            # If response payload empty, fallback
            return await self.fallback.generate_response(system_instruction, user_prompt, context)
            
        except Exception:
            # Graceful fallback on network/API failure
            return await self.fallback.generate_response(system_instruction, user_prompt, context)
