"""Wrappers simples et uniformes autour des SDK Anthropic et Mistral."""
from __future__ import annotations

from anthropic import Anthropic
from mistralai import Mistral


class ClaudeClient:
    """Petit wrapper autour du SDK officiel Anthropic."""

    def __init__(self, api_key: str, model: str = "claude-opus-4-8") -> None:
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def ask(self, prompt: str, system: str | None = None, max_tokens: int = 1024) -> str:
        """Une question simple → une réponse texte."""
        kwargs: dict = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system
        resp = self.client.messages.create(**kwargs)
        return "".join(b.text for b in resp.content if b.type == "text").strip()

    def chat(self, messages: list[dict], system: str | None = None, max_tokens: int = 1024) -> str:
        """Conversation multi-tours (liste de messages role/content)."""
        kwargs: dict = {"model": self.model, "max_tokens": max_tokens, "messages": messages}
        if system:
            kwargs["system"] = system
        resp = self.client.messages.create(**kwargs)
        return "".join(b.text for b in resp.content if b.type == "text").strip()


class MistralClient:
    """Petit wrapper autour du SDK officiel Mistral."""

    def __init__(self, api_key: str, model: str = "mistral-large-latest") -> None:
        self.client = Mistral(api_key=api_key)
        self.model = model

    def ask(self, prompt: str, system: str | None = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        resp = self.client.chat.complete(model=self.model, messages=messages)
        return resp.choices[0].message.content.strip()

    def chat(self, messages: list[dict]) -> str:
        resp = self.client.chat.complete(model=self.model, messages=messages)
        return resp.choices[0].message.content.strip()
