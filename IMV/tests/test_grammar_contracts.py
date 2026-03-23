"""
test_grammar_contracts.py
Gate tests: TASK_1.1, 1.2, 1.3, 2.1, 2.2 — [P1] all must pass before Phase 2.
2026-03-22
"""
import sys
from pathlib import Path
_IMV_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_IMV_DIR))

import pytest
from core.grammar import validate, MAX_RECURSION_DEPTH
from core.taxonomy import check_refinement_type, LIBRARY_SCALAR_MIN


def test_bnf_contract_present():
    """TASK_1.1: BNF CONTRACT present in grammar.py source."""
    src = open(_IMV_DIR / "core" / "grammar.py").read()
    assert "SENTENCE    ::=" in src
    assert "LIBRARY     ::=" in src
    assert "DEPTH_MAX: 64" in src


def test_max_recursion_constant():
    """TASK_1.2: MAX_RECURSION_DEPTH == 64."""
    assert MAX_RECURSION_DEPTH == 64


def test_decidability_guard_triggers():
    """TASK_1.2: validate() aborts at depth 64."""
    r = validate("TRUST FOUNDATION =><= .. verifica .. [scope] --[As de Guía] [term]", _depth=64)
    assert r.result.value == "INVALID"
    assert any("64" in e or "ABORT" in e or "H06" in e for e in r.errors)


def test_valid_sentence_depth_zero():
    """Regression: normal validate() still works after TASK_1.2."""
    r = validate("TRUST FOUNDATION =><= .. verifica .. [scope] --[As de Guía] [term]")
    assert r.result.value in ("VALID", "WARNING")


def test_refinement_trust_passes():
    """TASK_1.3: TRUST with S=0.93, foundation=True → passes."""
    ok, _ = check_refinement_type("TRUST", 0.93, True)
    assert ok is True


def test_refinement_trust_fails_scalar():
    """TASK_1.3: TRUST with S=0.80 → SCALAR_BELOW_MIN."""
    ok, reason = check_refinement_type("TRUST", 0.80, True)
    assert ok is False and "SCALAR_BELOW_MIN" in reason


def test_refinement_trust_fails_foundation():
    """TASK_1.3: TRUST with foundation=False → FOUNDATION_INVALID."""
    ok, reason = check_refinement_type("TRUST", 0.95, False)
    assert ok is False and "FOUNDATION_INVALID" in reason


def test_refinement_work_no_foundation():
    """TASK_1.3: WORK with S=0.82, foundation=False → passes."""
    ok, _ = check_refinement_type("WORK", 0.82, False)
    assert ok is True


def test_all_9_libraries_have_scalar_min():
    """TASK_1.3: all 9 standard libraries defined in LIBRARY_SCALAR_MIN."""
    for lib in ["TRUST","SAMU","CRYPTO","GATE","STACKING","WORK","SOCIAL","METHOD","ACTIVITY"]:
        assert lib in LIBRARY_SCALAR_MIN, f"{lib} missing"


def test_ports_importable():
    """TASK_2.1: core.ports imports cleanly, PORTS singleton exists."""
    from core.ports import PORTS, SentencePort, CrystalPort, ScalarPort
    assert PORTS is not None


def test_cli_adapter_is_sentence_port():
    """TASK_2.1: CLISentenceAdapter is a SentencePort — no direct grammar import in adapter."""
    from adapters.cli_adapter import CLISentenceAdapter
    from core.ports import SentencePort
    assert issubclass(CLISentenceAdapter, SentencePort)


def test_adapters_dont_import_grammar_directly():
    """TASK_2.1/GAP_4: adapters have no TOP-LEVEL samu/ledger imports (lazy ok)."""
    import ast
    for fname in ["adapters/cli_adapter.py", "adapters/db_adapter.py"]:
        src = open(_IMV_DIR / fname).read()
        tree = ast.parse(src)
        # Only check module-level imports (not inside functions/methods)
        top_imports = [
            n for n in ast.walk(tree)
            if isinstance(n, (ast.Import, ast.ImportFrom))
            and n.col_offset == 0
        ]
        top_names = []
        for n in top_imports:
            if isinstance(n, ast.ImportFrom) and n.module:
                top_names.append(n.module)
            elif isinstance(n, ast.Import):
                for alias in n.names:
                    top_names.append(alias.name)
        assert "core.samu" not in top_names, f"{fname}: top-level import of core.samu"
        assert "core.ledger" not in top_names, f"{fname}: top-level import of core.ledger"


def test_trust_context():
    """TASK_2.2: trust_context has correct SCALAR_MIN and REQUIRES_FOUNDATION."""
    from libraries.trust_context import LIBRARY_NAME, SCALAR_MIN, REQUIRES_FOUNDATION
    assert LIBRARY_NAME == "TRUST"
    assert SCALAR_MIN == 0.92
    assert REQUIRES_FOUNDATION is True


def test_gate_context_abort_codes():
    """TASK_2.2: gate_context exposes ABORT_CODES with H06."""
    from libraries.gate_context import ABORT_CODES
    assert "H06" in ABORT_CODES


def test_samu_context_delay():
    """TASK_2.2: samu_context has DELIBERATE_DELAY_SECONDS."""
    from libraries.samu_context import DELIBERATE_DELAY_SECONDS
    assert DELIBERATE_DELAY_SECONDS == 3


# ── Phase 3 tests ──────────────────────────────────────────────────────────

def test_pre_condition_1_min_tokens():
    """TASK_3.5: validate() rejects sentence with < 6 tokens."""
    r = validate("TRUST FOUNDATION verifica")
    assert r.result.value == "INVALID"
    assert any("PRE_1" in e or "6 tokens" in e for e in r.errors)


def test_pre_condition_2_bracket():
    """TASK_3.5: validate() rejects sentence without brackets."""
    r = validate("TRUST FOUNDATION =><= verifica scope Ballestrinque term")
    assert r.result.value == "INVALID"
    assert any("PRE_2" in e or "bracket" in e for e in r.errors)


def test_event_sourcing_types_exist():
    """TASK_2.3: TransactionType enum has 6 new event-sourcing entries."""
    from core.ledger import TransactionType
    new_types = [
        "SENTENCE_SUBMITTED", "GRAMMAR_VALIDATED", "SAMU_APPROVED",
        "CRYSTAL_WRITTEN", "SCALAR_UPDATED", "TERM_EXPIRED"
    ]
    existing = [t.value for t in TransactionType]
    for nt in new_types:
        assert nt in existing, f"{nt} missing from TransactionType"


def test_ledger_has_record_event():
    """TASK_2.3: HLFabric has record_event() and get_history() methods."""
    from core.ledger import HLFabric
    assert hasattr(HLFabric, "record_event")
    assert hasattr(HLFabric, "get_history")


def test_rag_cache_methods():
    """TASK_3.2: IMEBM25 has search_cached() and invalidate_cache()."""
    from core.rag import IMEBM25
    r = IMEBM25()
    assert hasattr(r, "search_cached")
    assert hasattr(r, "invalidate_cache")
    assert hasattr(r, "_corpus_fingerprint")


def test_rag_incremental_methods():
    """TASK_3.4: IMEBM25 has build_incremental() method."""
    from core.rag import IMEBM25
    assert hasattr(IMEBM25(), "build_incremental")


def test_sovereign_monad_bind():
    """TASK_3.1: SovereignResult.bind() short-circuits on invalid."""
    from core.foundation import SovereignResult
    failing = SovereignResult(value=None, scalar=0.5, term_active=False,
                              library="TRUST", error="test")
    result = failing.bind(lambda r: SovereignResult.unit("should_not_reach", 0.9, "TRUST"))
    assert result.error == "test"  # propagated, fn not called


def test_sovereign_monad_unit():
    """TASK_3.1: SovereignResult.unit() creates valid monad."""
    from core.foundation import SovereignResult
    r = SovereignResult.unit("value", 0.92, "TRUST")
    assert r.is_valid and r.value == "value"


def test_algebraic_effect_denied():
    """TASK_3.3: check_effect() denies EMIT_WU when scalar < 0.85."""
    from core.samu import SamuEffect, check_effect
    ok, reason = check_effect(SamuEffect.EMIT_WU, term_active=True, scalar=0.80)
    assert ok is False and "EFFECT_DENIED" in reason


def test_algebraic_effect_allowed():
    """TASK_3.3: check_effect() allows READ_SCALAR always."""
    from core.samu import SamuEffect, check_effect
    ok, _ = check_effect(SamuEffect.READ_SCALAR, term_active=False, scalar=0.0)
    assert ok is True


def test_gap9_glossary_builder_exists():
    """GAP_9: tools/glossary_builder.py exists and is importable."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from tools.glossary_builder import build_glossary, write_glossary
    assert callable(build_glossary)
    assert callable(write_glossary)


def test_gap9_glossary_parses_terms():
    """GAP_9: glossary builder finds LACHO library terms."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from tools.glossary_builder import build_glossary
    g = build_glossary()
    assert g["meta"]["total_terms"] > 50, "Expected > 50 terms parsed"
    assert g["meta"]["files_scanned"] > 0


def test_gap9_activity_has_verbs():
    """GAP_9: ACTIVITY term parsed with correct verbs."""
    import sys, json
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    output = Path(__file__).parent.parent / "data" / "glossary_unified.json"
    if not output.exists():
        from tools.glossary_builder import write_glossary
        write_glossary()
    data = json.loads(output.read_text())
    activity = data["terms"].get("ACTIVITY", {})
    verbs = activity.get("verbs", [])
    assert "inicia" in verbs or "cristaliza" in verbs, f"Expected ACTIVITY verbs, got {verbs}"
