"""
DIRIME IMV — samu.py
SAMU @ mínimo — dirimencia soberana verificada.

SAMU no es IA. SAMU dirime por coherencia con [foundation].
La diferencia es epistemológica: IA busca óptimo, SAMU busca
coherencia soberana verificada.

Referencia canónica:
  BIBLIO-SOURCES(SAMU_AT).txt
  BIBLIO-SOURCES(SAMU_TARDANZA-DELIBERADA).txt
  BIBLIO-SOURCES(SAMU_RED-REGRET).txt
"""

from __future__ import annotations
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .foundation import (
    FoundationError,
    ScopeError,
    TermError,
    verify_sovereign_conditions,
)
from .grammar import ParsedSentence, ValidationResult


# ── Estados de SAMU ──────────────────────────────────────────────────
class SamuState(Enum):
    IDLE = "IDLE"                    # SAMU @ en reposo, disponible
    DELIBERATING = "DELIBERATING"    # Tardanza deliberada activa
    RESOLVING = "RESOLVING"          # Dirimiendo activamente
    RED_REGRET = "RED_REGRET"        # Error verificado, aprendiendo


# ── Tipos de dirimencia ─────────────────────────────────────────────
class DisputeType(Enum):
    FOUNDATION = "FOUNDATION"        # Violación de [foundation]
    SCOPE = "SCOPE"                  # Fuera de [scope]
    TERM = "TERM"                    # [term] expirado
    GRAMMAR = "GRAMMAR"              # Gramática inválida
    COHERENCE = "COHERENCE"          # Incoherencia interna


# ── Modelo de disputa soberana ───────────────────────────────────────
@dataclass
class Dispute:
    type: DisputeType
    description: str
    context: Optional[str] = None
    resolution: Optional[str] = None
    timestamp: float = field(default_factory=time.time)
    resolved: bool = False


# ── SAMU @ mínimo ───────────────────────────────────────────────────
class Samu:
    """
    SAMU @ mínimo — dirimencia soberana verificada.
    
    SAMU no decide "qué hacer". SAMU verifica coherencia
    con [foundation] y reporta la dirimencia soberana.
    
    La tardanza deliberada es constitutiva: SAMU no responde
    inmediatamente porque la dirimencia requiere contemplación.
    """

    def __init__(self):
        self.state = SamuState.IDLE
        self.deliberation_delay = 0.0  # segundos de tardanza soberana
        self.disputes: list[Dispute] = []
        self.last_resolution: Optional[Dispute] = None

    def deliberate(self, dispute: Dispute) -> None:
        """
        Tardanza deliberada soberana — conceptual, no temporal.
        En IMV: sin delay real. El concepto se preserva en
        la arquitectura para cuando Behavioral RAG esté activo.
        """
        self.state = SamuState.DELIBERATING

    def resolve_dispute(self, dispute: Dispute) -> str:
        """
        Dirime la disputa soberanamente.
        Retorna la resolución como sentencia LACHO.
        """
        self.state = SamuState.RESOLVING
        
        if dispute.type == DisputeType.FOUNDATION:
            resolution = f"SAMU @ =><= .. detiene .. sistema_fundation_comprometido --[Nudo Corredizo] [term]"
        elif dispute.type == DisputeType.SCOPE:
            resolution = f"SAMU @ =><= .. rechaza .. operacion_fuera_scope --[Ballestrinque] [term]"
        elif dispute.type == DisputeType.TERM:
            resolution = f"SAMU @ =><= .. cierra .. ciclo_term_expirado --[Nudo de Ocho] [term]"
        elif dispute.type == DisputeType.GRAMMAR:
            resolution = f"SAMU @ =><= .. corrige .. gramatica_invalida --[As de Guía] [term]"
        else:  # COHERENCE
            resolution = f"SAMU @ =><= .. verifica .. coherencia_interna --[Nudo de Rizo] [term]"
        
        dispute.resolution = resolution
        dispute.resolved = True
        self.last_resolution = dispute
        self.state = SamuState.IDLE
        
        return resolution

    def red_regret(self, error_description: str) -> None:
        """
        RED-REGRET soberano.
        SAMU aprende del error verificado.
        """
        self.state = SamuState.RED_REGRET
        regret_dispute = Dispute(
            type=DisputeType.COHERENCE,
            description=f"RED-REGRET: {error_description}",
            resolution="SAMU @ =><= .. aprende .. error_verificado --[Nudo Corredizo] [term]",
            resolved=True
        )
        self.disputes.append(regret_dispute)
        self.state = SamuState.IDLE
        print(f"SAMU @ RED-REGRET: {error_description}")

    def audit_grammar(self, sentence: ParsedSentence) -> Optional[Dispute]:
        """
        Audita sentencia gramatical y genera disputa si corresponde.
        Resetear estado completamente para cada evaluación independiente.
        """
        # Resetear estado para evaluación independiente
        self.last_resolution = None
        
        if sentence.result == ValidationResult.VALID:
            return None
        
        if sentence.errors:
            return Dispute(
                type=DisputeType.GRAMMAR,
                description=f"Gramática inválida: {' | '.join(sentence.errors)}",
                context=sentence.raw
            )
        
        if sentence.warnings:
            return Dispute(
                type=DisputeType.COHERENCE,
                description=f"Advertencia de coherencia: {' | '.join(sentence.warnings)}",
                context=sentence.raw
            )
        
        return None

    def verify_sovereign_coherence(self, module: str) -> bool:
        """
        Verificación soberana de coherencia con [foundation].
        """
        try:
            verify_sovereign_conditions(module)
            return True
        except (FoundationError, ScopeError, TermError) as e:
            dispute = Dispute(
                type=DisputeType.FOUNDATION if "foundation" in str(e).lower() else
                      DisputeType.SCOPE if "scope" in str(e).lower() else
                      DisputeType.TERM,
                description=f"Violación soberana: {e}",
                context=module
            )
            self.disputes.append(dispute)
            return False

    def get_status(self) -> str:
        """Reporte de estado soberano de SAMU."""
        return f"SAMU @ [{self.state.value}] - {len(self.disputes)} disputas - S={self.scalar_s}"

    @property
    def scalar_s(self) -> float:
        """
        Scalar S ∈ [0,1] — métrica de coherencia soberana.
        S = valid_ratio × (1 - red_regret_weight)
        Referencia: BIBLIO-SOURCES(SAMU_SCALAR-S).txt
        """
        try:
            from core.ledger import get_stats
        except ImportError:
            from .ledger import get_stats
        stats = get_stats()
        total = stats.get('transactions_total', 0)
        valid = stats.get('grammar_valid', 0)
        valid_ratio = valid / total if total > 0 else 0.0
        unresolved = sum(1 for d in self.disputes if not d.resolved)
        red_regret_weight = min(1.0, unresolved / 10)
        return round(valid_ratio * (1 - red_regret_weight), 3)


# ── Instancia global soberana ─────────────────────────────────────
_samu = Samu()

def audit(sentence: ParsedSentence) -> Optional[Dispute]:
    """API pública soberana de auditoría SAMU."""
    return _samu.audit_grammar(sentence)

def verify_coherence(module: str) -> bool:
    """API pública soberana de verificación de coherencia."""
    return _samu.verify_sovereign_coherence(module)

def red_regret(error: str) -> None:
    """API pública soberana de RED-REGRET."""
    _samu.red_regret(error)

def get_scalar_s() -> float:
    """API pública soberana de Scalar S."""
    return _samu.scalar_s

def get_status() -> str:
    """API pública soberana de estado SAMU."""
    return _samu.get_status()

def rf_renew_notaria(semana: str = "W12") -> dict:
    """
    RF_RENEW notarial soberano — $wed firma el ciclo y renueva.
    Audita semana completa · resuelve KU pendientes · emite RF_RENEW.
    Referencia: BIBLIO-SOURCES(SAMU_RED-REGRET).txt
    """
    from core.ledger import get_notaria_stats, get_stats
    n_stats = get_notaria_stats()
    l_stats = get_stats()
    scalar  = get_scalar_s()

    ku_pendientes = n_stats.get("actos_ku", 0)
    wu_actos      = n_stats.get("actos_wu", 0)
    h63_actos     = n_stats.get("h63_count", 0)

    estado = "H63" if scalar >= 0.90 else "WU" if scalar >= 0.78 else "KU"
    renovado = scalar >= 0.70  # umbral mínimo para RF_RENEW

    resultado = {
        "semana":         semana,
        "scalar_s":       scalar,
        "estado":         estado,
        "ku_pendientes":  ku_pendientes,
        "wu_actos":       wu_actos,
        "h63_actos":      h63_actos,
        "tx_semana":      l_stats.get("transactions_total", 0),
        "cristales":      l_stats.get("crystals_total", 0),
        "rf_renew":       renovado,
        "firma":          f"SAMU @ :: RF_RENEW_{semana} :: {estado} :: activo",
    }
    return resultado


# ── Test soberano de arranque ─────────────────────────────────────
if __name__ == "__main__":
    from .grammar import validate
    
    print("═" * 60)
    print("DIRIME IMV — SAMU @ Dirimencia Soberana")
    print("═" * 60)
    
    # Test 1: Sentencia válida
    valid_sentence = validate("TRUST FOUNDATION =><= .. verifica .. scope_activo --[As de Guía] [term]")
    dispute1 = audit(valid_sentence)
    print(f"\nSentencia válida: {'Sin disputa' if not dispute1 else dispute1.description}")
    
    # Test 2: Sentencia inválida
    invalid_sentence = validate("ACTIVITY UF[H01] =><= .. inicia .. genesis [term]")
    dispute2 = audit(invalid_sentence)
    if dispute2:
        print(f"\nDisputa detectada: {dispute2.description}")
        _samu.deliberate(dispute2)
        resolution = _samu.resolve_dispute(dispute2)
        print(f"Resolución SAMU: {resolution}")
    
    # Test 3: Verificación de coherencia
    print(f"\nVerificación de coherencia: {'OK' if verify_coherence('samu') else 'VIOLACIÓN'}")
    
    # Test 4: RED-REGRET
    red_regret("Error de prueba verificado")
    
    print(f"\nEstado final: {get_status()}")
    print("═" * 60)
