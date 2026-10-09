from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .config import Settings


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings.from_env()

    def _request(self, path: str, payload: dict | None = None) -> dict:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            self.settings.base_url + path,
            data=data,
            headers={"Content-Type": "application/json"},
            method="GET" if data is None else "POST",
        )
        try:
            with urlopen(request, timeout=self.settings.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:500]
            raise OllamaError(f"Ollama HTTP {exc.code}: {body}") from exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise OllamaError(f"无法连接 Ollama：{exc}") from exc

    def version(self) -> str:
        return str(self._request("/api/version").get("version", "unknown"))

    def models(self) -> list[str]:
        return [str(item.get("name")) for item in self._request("/api/tags").get("models", []) if item.get("name")]

    def chat(self, prompt: str, *, system: str | None = None, model: str | None = None) -> str:
        if not prompt.strip():
            raise ValueError("问题不能为空")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        result = self._request("/api/chat", {"model": model or self.settings.model, "messages": messages, "stream": False})
        answer = result.get("message", {}).get("content")
        if not isinstance(answer, str):
            raise OllamaError("Ollama 返回内容缺少 message.content")
        return answer
