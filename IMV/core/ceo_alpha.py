"""
DIRIME IMV — ceo_alpha.py
CEO ALPHA H64 — jerarquía soberana 67 roles × Unicode China
[term] :: activo
"""
from __future__ import annotations
import json
from pathlib import Path

_CEO_PATH = Path(__file__).parent.parent / "config" / "CEO_ALPHA_H64.json"
_CEO_DATA: dict | None = None


def load_ceo_alpha() -> dict:
    global _CEO_DATA
    if _CEO_DATA is None:
        try:
            _CEO_DATA = json.loads(_CEO_PATH.read_text(encoding="utf-8"))
        except Exception:
            _CEO_DATA = {"niveles": []}
    return _CEO_DATA


def get_role_by_hexagram(h_num: str) -> dict | None:
    # H63 既濟 NOTARIO 公证员 · $thu 2026-03-12
    # acto notarial = DIR(CLOSE) soberano · Scalar S ≥ 0.90
    data = load_ceo_alpha()
    hexagrams = data.get("hexagrams", {})
    entry = hexagrams.get(h_num)
    if entry:
        return {"hexagrama": h_num, **entry}
    return None

def get_scalar_threshold(h_num: str) -> float:
    role = get_role_by_hexagram(h_num)
    if role:
        t = role.get("threshold", "")
        thresholds = {
            "arranque": 0.95, "optimo": 0.92, "decision": 0.90,
            "custodia": 0.88, "riesgo": 0.85, "ciclo": 0.84,
            "fuente": 0.82, "quietud": 0.80,
        }
        return thresholds.get(t, 0.80)
    return 0.80

def ceo_summary() -> str:
    data = load_ceo_alpha()
    total = len(data.get("hexagrams", {}))
    return f"CEO ALPHA: {total} hexagramas cargados · v{data.get('version','?')}"


def get_unicode_tokens_for_role(h_num: str) -> list:
    """Tokens Unicode operativos del rol."""
    role = get_role_by_hexagram(h_num)
    return role.get("unicode_tokens", []) if role else []


def get_sentence_for_role(h_num: str) -> str:
    """Sentencia LACHO canónica del rol."""
    role = get_role_by_hexagram(h_num)
    return role.get("sentencia", "") if role else ""


if __name__ == "__main__":
    print(ceo_summary())
    # Test H01
    r = get_role_by_hexagram("H01")
    if r:
        print(f"H01: {r.get('nombre','?')} · threshold={get_scalar_threshold('H01')}")
        print(f"H01: {get_sentence_for_role('H01')}")
