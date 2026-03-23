"""
DIRIME_v2 — ollama/bridge_ollama.py
Bridge Ollama soberano — NL → LACHO via Ollama local.
Compatible con qwen2.5:3b y otros modelos locales.
"""
from __future__ import annotations
import json
import httpx
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent.parent.parent / "IMV" / "config" / "ollama.json"

def get_config() -> dict:
    """Retorna configuración de Ollama. {} si no disponible."""
    if not _CONFIG_PATH.exists():
        return {
            "provider": "ollama",
            "model": "qwen2.5:0.5b",  # Modelo más pequeño y controlable
            "base_url": "http://localhost:11434",
            "timeout": 30
        }
    try:
        return json.loads(_CONFIG_PATH.read_text())
    except Exception:
        return {
            "provider": "ollama", 
            "model": "qwen2.5:3b",
            "base_url": "http://localhost:11434",
            "timeout": 30
        }

def is_active() -> bool:
    """True si Ollama está activo y respondiendo."""
    try:
        cfg = get_config()
        response = httpx.get(f"{cfg['base_url']}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def translate(natural_text: str, system_prompt: str) -> str | None:
    """
    Envía texto natural + system_prompt a Ollama.
    Retorna sentencia LACHO o None si falla.
    """
    if not is_active():
        return None
    
    try:
        cfg = get_config()
        
        # Para Ollama, usar prompt más directo que force la estructura
        direct_prompt = f"""Convierte "{natural_text}" a gramática LACHO exacta:

REGLAS:
- Biblioteca: TRUST, SOCIAL, CRYPTO, WORK, SAMU, ACTIVITY, GATE, STACKING, METHOD
- Formato: BIBLIOTECA SUJETO =><= .. verbo .. objeto --[Nudo] [term]
- Nudos: As de Guía, Nudo de Ocho, Ballestrinque, Nudo Corredizo, Nudo de Rizo

Ejemplo: "certificar acto" → CRYPTO (spark seat) =><= .. certifica .. acto --[As de Guía] [term]

Tu respuesta (SOLO la sentencia LACHO):"""
        
        response = httpx.post(
            f"{cfg['base_url']}/api/generate",
            timeout=cfg.get("timeout", 30),
            json={
                "model": cfg.get("model", "qwen2.5:0.5b"),
                "prompt": direct_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0,  # Máxima precisión para gramática LACHO
                    "top_p": 0.8,
                    "max_tokens": 200
                }
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        return None
        
    except Exception as e:
        print(f"Error Ollama: {e}")
        return None

def list_models() -> list[str]:
    """Lista modelos disponibles en Ollama."""
    try:
        cfg = get_config()
        response = httpx.get(f"{cfg['base_url']}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        return []
    except Exception:
        return []

# Alias para compatibilidad con bridge.py
def get_provider_name() -> str:
    return "ollama"

def get_model_name() -> str:
    cfg = get_config()
    return cfg.get("model", "qwen2.5:3b")
