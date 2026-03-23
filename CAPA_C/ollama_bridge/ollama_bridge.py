# ── DIRIME_v3/ollama_bridge/ollama_bridge.py ──────────────────
"""
DIRIME v3 — ollama_bridge.py
Swap transparente Groq → Ollama local
ESTADO: STUB · activar cuando PC Ryzen operativa
Referencia: UNICODE_DIRIME_V3.txt · README_CAPA_C.md
[term] :: activo
"""
from __future__ import annotations
from dataclasses import dataclass

BRIDGE_ACTIVE = False  # activar cuando Ryzen disponible


@dataclass
class BridgeResponse:
    content: str
    model: str
    source: str  # "groq" | "ollama"
    tokens_used: int = 0


class OllamaBridge:
    """
    Swap transparente Groq → Ollama.
    Mismo contrato API que chat.py → _translate_via_api().
    """
    MODEL = "llama3.3:70b"
    ENDPOINT = "http://localhost:11434/api/chat"

    def __init__(self):
        self.active = BRIDGE_ACTIVE

    def chat(self, messages: list[dict], system: str = "") -> BridgeResponse:
        """
        Equivalente a Groq._translate_via_api().
        Cuando activo: llama a Ollama local.
        Cuando inactivo: NotImplementedError → fallback a Groq.
        """
        if not self.active:
            raise NotImplementedError(
                "OllamaBridge inactivo — PC Ryzen pendiente. "
                "Usar Groq: chat.py → _translate_via_api()"
            )
        # TODO: implementar cuando Ryzen disponible
        # import requests
        # resp = requests.post(self.ENDPOINT, json={...})
        raise NotImplementedError("CAPA C: implementar post Ryzen")

    def is_available(self) -> bool:
        """Verifica si Ollama local responde."""
        if not self.active:
            return False
        try:
            import requests
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            return r.status_code == 200
        except Exception:
            return False


# [term] :: activo · bridge•ollama•cat_os•ime_local
