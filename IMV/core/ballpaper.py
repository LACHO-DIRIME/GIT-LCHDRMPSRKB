"""
IMV/core/ballpaper.py
BALLPAPER — tabla 3 familias · assign_unicode_token()
DIRIME IMV · soberanía operativa
[term] :: activo · [seal of secrecy] :: activo
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

# ── TABLA 3 FAMILIAS ─────────────────────────────────────────────────────────
# Familia 1: ACCIÓN SOBERANA
# Familia 2: REGISTRO INMUTABLE
# Familia 3: AUDITORÍA / DIRIMENCIA

FAMILIA_1_ACCION = {
    "certifica":    ("CRYPTO",   "(spark seat)", "H63", 0.92),
    "sella":        ("STACKING", "UF[H63]",      "H63", 0.95),
    "verifica":     ("TRUST",    "FOUNDATION",   "H61", 0.88),
    "ejecuta":      ("WORK",     "{actuator}",   "H51", 0.85),
    "transmite":    ("SOCIAL",   "{relay}",      "H08", 0.85),
    "conduce":      ("TRUST",    "[logistical-executive]", "H03", 0.88),
    "orquesta":     ("TRUST",    "[logistical-executive]", "H57", 0.88),
    "alerta":       ("TRUST",    "[logistical-executive]", "H06", 0.88),
}

FAMILIA_2_REGISTRO = {
    "inmutabiliza": ("STACKING", "UF[H52]",      "H52", 0.95),
    "cristaliza":   ("STACKING", "UF[H52]",      "H52", 0.90),
    "acumula":      ("STACKING", "UF[H48]",      "H48", 0.88),
    "registra":     ("WORK",     "{actuator}",   "H49", 0.85),
    "indexa":       ("METHOD",   "<stat_onto>",  "H60", 0.88),
    "trazabiliza":  ("TRUST",    "[logistical-executive]", "H35", 0.88),
}

FAMILIA_3_AUDITORIA = {
    "dirime":       ("SAMU",     "@",            "H06", 0.90),
    "audita":       ("SAMU",     "@",            "H61", 0.90),
    "arbitra":      ("SAMU",     "@",            "H15", 0.88),
    "evalúa":       ("SAMU",     "@",            "H29", 0.88),
    "calcula":      ("METHOD",   "<stat_onto>",  "H60", 0.88),
    "clasifica":    ("METHOD",   "<equation>",   "H30", 0.88),
}

ALL_FAMILIES = {**FAMILIA_1_ACCION, **FAMILIA_2_REGISTRO, **FAMILIA_3_AUDITORIA}


@dataclass
class UnicodeToken:
    verb:      str
    library:   str
    subject:   str
    hexagram:  str
    min_score: float
    familia:   int  # 1, 2 o 3


def assign_unicode_token(verb: str) -> Optional[UnicodeToken]:
    """
    Dado un verbo canónico LACHO, retorna su UnicodeToken soberano.
    Usado por ledger.py al cristalizar un verbo frecuente.
    Retorna None si el verbo no está en ninguna familia.
    """
    verb_lower = verb.lower().strip()

    if verb_lower in FAMILIA_1_ACCION:
        lib, subj, hex_, score = FAMILIA_1_ACCION[verb_lower]
        return UnicodeToken(verb_lower, lib, subj, hex_, score, 1)

    if verb_lower in FAMILIA_2_REGISTRO:
        lib, subj, hex_, score = FAMILIA_2_REGISTRO[verb_lower]
        return UnicodeToken(verb_lower, lib, subj, hex_, score, 2)

    if verb_lower in FAMILIA_3_AUDITORIA:
        lib, subj, hex_, score = FAMILIA_3_AUDITORIA[verb_lower]
        return UnicodeToken(verb_lower, lib, subj, hex_, score, 3)

    return None


def get_familia(n: int) -> dict:
    """Retorna la familia completa por número (1, 2 o 3)."""
    return {1: FAMILIA_1_ACCION, 2: FAMILIA_2_REGISTRO, 3: FAMILIA_3_AUDITORIA}.get(n, {})


def ballpaper_render(verb: str, scalar: float, estado: str = "") -> str:
    """
    Render ASCII del ballpaper para un verbo + scalar.
    Usado por chat.py y _show_notaria_status.
    """
    token = assign_unicode_token(verb)
    THRESH_H63 = 0.90
    filled = int(scalar / THRESH_H63 * 20)
    bar = "█" * min(filled, 20) + "░" * (20 - min(filled, 20))
    lib_str  = token.library  if token else "—"
    hex_str  = token.hexagram if token else "—"
    fam_str  = f"F{token.familia}" if token else "—"
    lines = [
        "┌─ BALLPAPER ──────────────────────────────┐",
        f"│ VERBO  : {verb:<34}│",
        f"│ LIB    : {lib_str:<34}│",
        f"│ HEX    : {hex_str:<34}│",
        f"│ FAMILIA: {fam_str:<34}│",
        f"│ S      : {scalar:.3f}  [{bar}] │",
        f"│ ESTADO : {estado or ('H63 ✅' if scalar >= THRESH_H63 else 'WU ⚡' if scalar >= 0.78 else 'KU ⏳'):<34}│",
        "└──────────────────────────────────────────┘",
    ]
    return "\n".join(lines)


def ballpaper_render_notaria(acto: str, resultado_samu: str, scalar_s: float) -> str:
    """
    Render ASCII específico para actos notariales.
    Usado por _show_notaria_status y endpoints /api/notaria/*.
    """
    THRESH_H63 = 0.90
    filled = int(scalar_s / THRESH_H63 * 20)
    bar = "█" * min(filled, 20) + "░" * (20 - min(filled, 20))
    lines = [
        "┌─ NOTARIA BALLPAPER ──────────────────────┐",
        f"│ ACTO   : {acto[:34]:<34}│",
        f"│ SAMU   : {resultado_samu[:34]:<34}│",
        f"│ S      : {scalar_s:.3f}  [{bar}] │",
        f"│ H63    : {'既濟 SELLADO ✅' if scalar_s >= THRESH_H63 else 'pendiente ⏳':<34}│",
        "└──────────────────────────────────────────┘",
    ]
    return "\n".join(lines)
