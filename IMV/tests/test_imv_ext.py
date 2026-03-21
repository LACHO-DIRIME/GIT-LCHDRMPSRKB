#!/usr/bin/env python3
"""
test_imv_ext.py — Tests extensión IMV · $fri 17/04
Lleva pytest de 27 → 33 tests soberanos
Referencia: test_imv.py · grammar.py · language_routing.py
"""
import pytest
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from core.grammar import validate, lacho_score, ValidationResult, GrammarValidator
from core.language_routing import route, route_batch


# ── TEST 28: SOCIAL {relay} válido ─────────────────────────────
def test_ext_social_relay():
    """SOCIAL {relay} es módulo válido en grammar · shard/relay semana"""
    s = "SOCIAL {relay} =><= .. lanza .. relay_kalil_nodos --[As de Guía] [term]"
    r = validate(s)
    assert r.result != ValidationResult.INVALID, f"SOCIAL relay debe ser válido: {r.errors}"


# ── TEST 29: METHOD <stat_onto> oracle ──────────────────────────
def test_ext_method_stat_onto():
    """METHOD <stat_onto> calcula oracle rating · threshold verificado"""
    s = "METHOD <stat_onto> =><= .. calcula .. oracle_nora_threshold_065 --[Ballestrinque] [term]"
    r = validate(s)
    assert r.result != ValidationResult.INVALID
    score = lacho_score(r)
    assert score >= 0.7, f"stat_onto score esperado >=0.7, got {score}"


# ── TEST 30: threshold en SAMU ──────────────────────────────────
def test_ext_samu_threshold():
    """SAMU @ audita threshold · threshold_cumplido_soberano"""
    s = "SAMU @ =><= .. audita .. threshold_score_s_target_0822 --[Ballestrinque] [term]"
    r = validate(s)
    assert r.result in (ValidationResult.VALID, ValidationResult.WARNING)


# ── TEST 31: STACKING UF[H04] shard ────────────────────────────
def test_ext_stacking_h04_shard():
    """STACKING UF[H04] reserva shard_corpus_slice_soberano"""
    s = "STACKING UF[H04] =><= .. reserva .. shard_corpus_slice_soberano --[Nudo de Ocho] [term]"
    r = validate(s)
    assert r.result != ValidationResult.INVALID


# ── TEST 32: TRUST FOUNDATION threshold ─────────────────────────
def test_ext_trust_threshold():
    """TRUST FOUNDATION verifica threshold_taxonomy_scalar_min"""
    s = "TRUST FOUNDATION =><= .. verifica .. threshold_taxonomy_scalar_min --[As de Guía] [term]"
    r = validate(s)
    assert r.result != ValidationResult.INVALID


# ── TEST 33: agents_kalil routing ───────────────────────────────
def test_ext_agents_kalil_routing():
    """Routing agents_kalil funciona con nueva extensión grammar"""
    sentences = [
        "SOCIAL {relay} =><= .. lanza .. ka_barrios_relay_community --[As de Guía] [term]",
        "METHOD <stat_onto> =><= .. calcula .. ka_nora_oracle_rating --[Ballestrinque] [term]",
        "TRUST FOUNDATION =><= .. verifica .. ka_threshold_taxonomy --[As de Guía] [term]"
    ]
    results = route_batch(sentences)
    assert len(results) == 3, f"Expected 3 routes, got {len(results)}"
    for r in results:
        assert r.success, f"Route failed: {r.error}"


# ── TEST 34: shard_corpus_slice ───────────────────────────────
def test_ext_shard_corpus_slice():
    """Shard corpus slice funciona con STACKING UF[H04]"""
    s = "STACKING UF[H04] =><= .. reserva .. shard_corpus_slice_BARRIOS --[Nudo de Ocho] [term]"
    r = validate(s)
    assert r.result != ValidationResult.INVALID
    score = lacho_score(r)
    assert score >= 0.8, f"shard score esperado >=0.8, got {score}"


# ── TEST 35: oracle_threshold_065 ───────────────────────────────
def test_ext_oracle_threshold_065():
    """Oracle threshold 0.65 validado correctamente"""
    s = "METHOD <stat_onto> =><= .. calcula .. oracle_threshold_065_valid --[Ballestrinque] [term]"
    r = validate(s)
    assert r.result != ValidationResult.INVALID
    assert "threshold_065" in r.object, "threshold_065 debe estar en objeto"


# ── TEST 36: Scalar_KALIL consolidación ─────────────────────────
def test_ext_scalar_kalil_consolidation():
    """Scalar_KALIL consolidación con METHOD <operator_flow>"""
    s = "METHOD <operator_flow> =><= .. opera .. scalar_kalil_consolidado --[Ballestrinque] [term]"
    r = validate(s)
    assert r.result != ValidationResult.INVALID


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
# [term] :: activo · shard•relay•oracle•threshold
