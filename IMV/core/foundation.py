"""
DIRIME IMV — foundation.py
[foundation] :: condiciones irreducibles de existencia soberana
[scope]      :: perímetro de operación declarado
[term]       :: horizonte temporal activo

Referencia canónica:
  BIBLIO-SOURCES(TRUST_FOUNDATION).txt
  BIBLIO-SOURCES(TRUST_SCOPE).txt
  BIBLIO-SOURCES(TRUST_TERM).txt
"""

from __future__ import annotations
import os
import sys
from functools import lru_cache
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


# ── Estados soberanos ────────────────────────────────────────────
class FoundationStatus(Enum):
    OK = "OK"
    DEGRADED = "DEGRADED"
    COMPROMISED = "COMPROMISED"


class ScopeStatus(Enum):
    ACTIVE = "ACTIVE"
    EXCEEDED = "EXCEEDED"
    UNDEFINED = "UNDEFINED"


class TermStatus(Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    OPEN = "OPEN"          # term declarado sin fecha límite


# ── Excepciones soberanas ─────────────────────────────────────────
class SovereignError(Exception):
    """Error base soberano — todo error DIRIME hereda de aquí."""
    pass


class FoundationError(SovereignError):
    """[foundation] violado — el suelo soberano está comprometido."""
    pass


class ScopeError(SovereignError):
    """[scope] excedido — la operación está fuera del perímetro soberano."""
    pass


class TermError(SovereignError):
    """[term] vencido — el horizonte temporal soberano expiró."""
    pass


# ── Modelos soberanos ─────────────────────────────────────────────
@dataclass
class Foundation:
    """
    [foundation] — condiciones irreducibles de existencia.
    Si COMPROMISED: todo se detiene. Sin excepción soberana.
    """
    status: FoundationStatus = FoundationStatus.OK
    identity_verified: bool = True
    corpus_accessible: bool = True
    ledger_available: bool = True
    notes: list[str] = field(default_factory=list)

    def is_operative(self) -> bool:
        """True solo si OK. DEGRADED permite operación limitada.
        COMPROMISED detiene todo soberanamente."""
        return self.status != FoundationStatus.COMPROMISED

    def verify(self) -> None:
        """Verificación soberana activa. Lanza FoundationError si compromised."""
        if self.status == FoundationStatus.COMPROMISED:
            raise FoundationError(
                f"[foundation] COMPROMISED — sistema detenido soberanamente. "
                f"Notas: {self.notes}"
            )


@dataclass
class Scope:
    """
    [scope] — perímetro soberano de operación.
    Toda verdad del sistema es local: declara su alcance o no es válida.
    """
    name: str = "IMV_core_modules"
    allowed_modules: list[str] = field(
        default_factory=lambda: ["grammar", "samu", "ledger", "chat"]
    )
    status: ScopeStatus = ScopeStatus.ACTIVE

    def contains(self, module: str) -> bool:
        """Verifica si un módulo está dentro del scope soberano."""
        return module in self.allowed_modules

    def verify(self, module: str) -> None:
        """Lanza ScopeError si el módulo está fuera del perímetro."""
        if self.status != ScopeStatus.ACTIVE:
            raise ScopeError(
                f"[scope] {self.status.value} — operación no permitida."
            )
        if not self.contains(module):
            raise ScopeError(
                f"Módulo '{module}' fuera de [scope] '{self.name}'. "
                f"Permitidos: {self.allowed_modules}"
            )


@dataclass
class Term:
    """
    [term] — horizonte temporal soberano.
    Todo ciclo debe poder cerrar. Sin [term] no hay ciclo válido.
    """
    label: str = "open"
    status: TermStatus = TermStatus.OPEN
    cycle_id: Optional[str] = None

    def is_active(self) -> bool:
        return self.status in (TermStatus.ACTIVE, TermStatus.OPEN)

    def verify(self) -> None:
        """Lanza TermError si el term expiró."""
        if self.status == TermStatus.EXPIRED:
            raise TermError(
                f"[term] '{self.label}' expirado — ciclo cerrado soberanamente."
            )


# ── Cargador desde config/ ────────────────────────────────────────
CONFIG_DIR = Path(__file__).parent.parent / "config"

def load_foundation() -> Foundation:
    """Carga [foundation] desde config/foundation.json."""
    cfg_path = CONFIG_DIR / "foundation.json"
    if not cfg_path.exists():
        return Foundation()  # defaults soberanos
    with open(cfg_path) as f:
        data = json.load(f)
    return Foundation(
        status=FoundationStatus(data.get("status", "OK")),
        identity_verified=data.get("identity_verified", True),
        corpus_accessible=data.get("corpus_accessible", True),
        ledger_available=data.get("ledger_available", True),
        notes=data.get("notes", []),
    )

def load_scope() -> Scope:
    """Carga [scope] desde config/scope.json."""
    cfg_path = CONFIG_DIR / "scope.json"
    if not cfg_path.exists():
        return Scope()
    with open(cfg_path) as f:
        data = json.load(f)
    return Scope(
        name=data.get("name", "IMV_core_modules"),
        allowed_modules=data.get("allowed_modules",
                                  ["grammar", "samu", "ledger", "chat"]),
        status=ScopeStatus(data.get("status", "ACTIVE")),
    )

def load_term() -> Term:
    """Carga [term] desde config/term.json."""
    cfg_path = CONFIG_DIR / "term.json"
    if not cfg_path.exists():
        return Term()
    with open(cfg_path) as f:
        data = json.load(f)
    return Term(
        label=data.get("label", "open"),
        status=TermStatus(data.get("status", "OPEN")),
        cycle_id=data.get("cycle_id"),
    )


# ── Verificación global soberana ─────────────────────────────────
@lru_cache(maxsize=1)
def verify_sovereign_conditions(module: str) -> tuple[Foundation, Scope, Term]:
    """
    Punto de entrada soberano para cualquier operación.
    Verifica [foundation], [scope] y [term] en ese orden.
    Lanza la excepción soberana correspondiente si algo falla.
    Retorna la tripla verificada si todo está OK.
    """
    foundation = load_foundation()
    scope = load_scope()
    term = load_term()

    foundation.verify()   # COMPROMISED detiene todo
    scope.verify(module)  # fuera de scope bloquea
    term.verify()         # term expirado bloquea

    return foundation, scope, term


# ── Config defaults para primer arranque ─────────────────────────
def init_config_defaults() -> None:
    """Crea config/*.json con valores soberanos por defecto si no existen."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    foundation_cfg = CONFIG_DIR / "foundation.json"
    if not foundation_cfg.exists():
        with open(foundation_cfg, "w") as f:
            json.dump({
                "status": "OK",
                "identity_verified": True,
                "corpus_accessible": True,
                "ledger_available": True,
                "notes": []
            }, f, indent=2)

    scope_cfg = CONFIG_DIR / "scope.json"
    if not scope_cfg.exists():
        with open(scope_cfg, "w") as f:
            json.dump({
                "name": "IMV_core_modules",
                "allowed_modules": ["grammar", "samu", "ledger", "chat"],
                "status": "ACTIVE"
            }, f, indent=2)

    term_cfg = CONFIG_DIR / "term.json"
    if not term_cfg.exists():
        with open(term_cfg, "w") as f:
            json.dump({
                "label": "open",
                "status": "OPEN",
                "cycle_id": None
            }, f, indent=2)
