"""LLM provider abstraction: anthropic | ollama | mock. Real providers fall back to the mock
provider if the call fails, so the demo never breaks when a key/server is missing."""

from __future__ import annotations

import json
import logging
import os
import re
from abc import ABC, abstractmethod
from collections.abc import Iterator

logger = logging.getLogger("learning_dna.llm")


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_message: str) -> str: ...

    @abstractmethod
    def stream(self, system_prompt: str, user_message: str) -> Iterator[str]: ...


class MockProvider(LLMProvider):
    """Offline provider: builds a DNA-aware answer from the retrieved context in the prompt."""

    def _answer(self, system_prompt: str, user_message: str) -> str:
        ctx = system_prompt.split("Context:", 1)[-1] if "Context:" in system_prompt else ""
        snippets = [ln[2:].strip() for ln in ctx.splitlines() if ln.startswith("- ")]
        fmt = re.search(r"Preferred Format: (.+)", system_prompt)
        span = re.search(r"Attention Span: ([\d.]+)", system_prompt)
        pace = re.search(r"Learning Pace: (.+)", system_prompt)
        if not snippets:
            return ("I couldn't find this in your study material yet. Try uploading a document on the topic, "
                    "or rephrase the question - for example, name the concept you are studying.")
        text = snippets[0]
        if len(snippets) > 1:
            text += "\n\nRelated: " + snippets[1]
        tips = []
        if fmt:
            tips.append(f"Since you learn best with {fmt.group(1).strip().lower()} material, try a worked example or diagram next.")
        if span and float(span.group(1)) and float(span.group(1)) < 30:
            tips.append("Your attention span is on the shorter side, so study this in a 20-minute block.")
        if pace and pace.group(1).strip().lower() == "slow":
            tips.append("Take it step by step and re-check the prerequisites first.")
        return text + ("\n\n" + " ".join(tips) if tips else "")

    def generate(self, system_prompt: str, user_message: str) -> str:
        return self._answer(system_prompt, user_message)

    def stream(self, system_prompt: str, user_message: str) -> Iterator[str]:
        for word in self._answer(system_prompt, user_message).split(" "):
            yield word + " "


class AnthropicProvider(LLMProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5-5")
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        import anthropic  # lazy import
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate(self, system_prompt: str, user_message: str) -> str:
        msg = self.client.messages.create(model=self.model, max_tokens=800, system=system_prompt,
                                          messages=[{"role": "user", "content": user_message}])
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")

    def stream(self, system_prompt: str, user_message: str) -> Iterator[str]:
        with self.client.messages.stream(model=self.model, max_tokens=800, system=system_prompt,
                                         messages=[{"role": "user", "content": user_message}]) as s:
            yield from s.text_stream


class OllamaProvider(LLMProvider):
    def __init__(self) -> None:
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL", "llama3")

    def _payload(self, system_prompt: str, user_message: str, stream: bool) -> dict:
        return {"model": self.model, "system": system_prompt, "prompt": user_message, "stream": stream}

    def generate(self, system_prompt: str, user_message: str) -> str:
        import httpx
        r = httpx.post(f"{self.host}/api/generate", json=self._payload(system_prompt, user_message, False), timeout=60)
        r.raise_for_status()
        return r.json().get("response", "")

    def stream(self, system_prompt: str, user_message: str) -> Iterator[str]:
        import httpx
        with httpx.stream("POST", f"{self.host}/api/generate",
                          json=self._payload(system_prompt, user_message, True), timeout=60) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    yield json.loads(line).get("response", "")


class FallbackProvider(LLMProvider):
    """Wraps a real provider; on any error answers with the mock provider instead."""

    def __init__(self, primary_factory, name: str) -> None:
        self.name = name
        self._factory = primary_factory
        self._mock = MockProvider()

    def generate(self, system_prompt: str, user_message: str) -> str:
        try:
            return self._factory().generate(system_prompt, user_message)
        except Exception as exc:
            logger.warning("%s failed (%s); using mock provider", self.name, exc)
            return self._mock.generate(system_prompt, user_message)

    def stream(self, system_prompt: str, user_message: str) -> Iterator[str]:
        started = False
        try:
            for chunk in self._factory().stream(system_prompt, user_message):
                started = True
                yield chunk
        except Exception as exc:
            logger.warning("%s stream failed (%s); using mock provider", self.name, exc)
            if not started:
                yield from self._mock.stream(system_prompt, user_message)


_anthropic_instance: AnthropicProvider | None = None


def _anthropic_provider() -> AnthropicProvider:
    """Create the Anthropic client once instead of on every request."""
    global _anthropic_instance
    if _anthropic_instance is None:
        _anthropic_instance = AnthropicProvider()
    return _anthropic_instance


def get_llm_provider() -> LLMProvider:
    provider = os.getenv("LLM_PROVIDER", "mock").lower()
    if provider == "anthropic":
        return FallbackProvider(_anthropic_provider, "anthropic")
    if provider == "ollama":
        return FallbackProvider(OllamaProvider, "ollama")
    return MockProvider()
