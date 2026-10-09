from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    base_url: str = "http://127.0.0.1:11434"
    model: str = "qwen2.5:7b"
    timeout: float = 120.0

    @classmethod
    def from_env(cls) -> "Settings":
        timeout = float(os.getenv("EARTHFIRE_TIMEOUT", "120"))
        if timeout <= 0 or timeout > 3600:
            raise ValueError("EARTHFIRE_TIMEOUT 必须在 0 到 3600 秒之间")
        return cls(
            base_url=os.getenv("OLLAMA_BASE_URL", cls.base_url).rstrip("/"),
            model=os.getenv("EARTHFIRE_MODEL", cls.model),
            timeout=timeout,
        )
