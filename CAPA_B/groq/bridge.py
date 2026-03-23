"""
DIRIME_v2 — groq/bridge.py
Bridge Groq soberano — NL → LACHO via API.
Extraído de IMV/interface/chat.py para módulo independiente.
Referencia: BIBLIO-SOURCES(DIRIME-IMV_CHAT).txt §3.2
"""
from __future__ import annotations
import json
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent.parent.parent / "IMV" / "config" / "api.json"
_CORPUS_PATH = Path(__file__).parent.parent.parent / "CORPUS"

def get_config() -> dict:
    """Retorna configuración del bridge. {} si no disponible."""
    if not _CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(_CONFIG_PATH.read_text())
    except Exception:
        return {}

def is_active() -> bool:
    """True si Groq está configurado y activo."""
    cfg = get_config()
    key = cfg.get("key", "")
    return (cfg.get("provider") == "groq"
            and bool(key)
            and not key.startswith("REEMPLAZAR"))

def translate(natural_text: str, system_prompt: str) -> str | None:
    """
    Envía texto natural + system_prompt a Groq.
    Retorna sentencia LACHO o None si falla.
    """
    if not is_active():
        return None
    try:
        import httpx
        cfg = get_config()
        response = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {cfg['key']}",
                "Content-Type": "application/json",
            },
            json={
                "model": cfg.get("model", "llama-3.3-70b-versatile"),
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": natural_text},
                ],
                "max_tokens": cfg.get("max_tokens", 150),
                "temperature": cfg.get("temperature", 0.1),
            },
            timeout=10.0,
        )
        if response.status_code != 200:
            return None
        result = response.json()["choices"][0]["message"]["content"].strip()
        if "=><=".strip() in result and "[term]" in result:
            return result
        return None
    except Exception:
        return None

def status() -> dict:
    """Estado del bridge para diagnóstico."""
    cfg = get_config()
    return {
        "active": is_active(),
        "provider": cfg.get("provider", "none"),
        "model": cfg.get("model", "none"),
        "key_set": bool(cfg.get("key", "")) and not cfg.get("key","").startswith("REEMPLAZAR"),
    }
