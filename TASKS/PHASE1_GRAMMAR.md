# TASKS/PHASE1_GRAMMAR.md
# [P1][I2] Grammar Hardening — Week 1, Days 2-3
# WHO: Windsurf writes · Claude audits · Gemini stress-tests
# GATE: all tasks complete before Phase 2

---

## TASK_1.1 — GRAMMAR_FORMALIZATION
### File: IMV/core/grammar.py
### Priority: [P1][I2] · Implication: AMBIGUOUS_GRAMMAR on new terms

Add this BNF docstring contract at the TOP of grammar.py, after the module docstring:

```python
"""
LACHO FORMAL GRAMMAR — BNF CONTRACT v1.0
Context-sensitive (Chomsky N3) — maps to LACHO sentence structure

SENTENCE    ::= LIBRARY SUBJECT BIND VERB OBJECT NUDO TERM
LIBRARY     ::= "TRUST" | "SAMU" | "CRYPTO" | "GATE" | "STACKING"
              | "WORK" | "SOCIAL" | "METHOD" | "ACTIVITY" | "COGNITIVO"
BIND        ::= "=><=">
NUDO        ::= "--[" NUDO_TYPE "]"
NUDO_TYPE   ::= "As de Guía" | "Ballestrinque" | "⊗" | "Corredizo"
TERM        ::= "[" IDENTIFIER "]"
ABORT       ::= "!!" "Abort" "!!" ("--" "--" IDENTIFIER)?
CONV_DEF    ::= IDENTIFIER "::=" EXPRESSION

SLOTS: exactly 6 mandatory positions before TERM
DEPTH_MAX: 64 (maps to 64 UF hexagrams)
ENCODING: UTF-8, CJK block U+4E00–U+9FFF supported
"""
```

Windsurf instruction: open IMV/core/grammar.py, locate the module docstring
(lines 1-12 approx), insert the BNF block immediately after it.

---

## TASK_1.2 — DECIDABILITY_GUARD
### File: IMV/core/grammar.py · function: validate()
### Priority: [P1][I1] · Implication: infinite loop in nested ANIDAR

Add recursion depth guard to validate():

```python
MAX_RECURSION_DEPTH = 64  # maps to 64 UF hexagrams — add as module constant

def validate(text: str, _depth: int = 0) -> ValidationResult:
    if _depth >= MAX_RECURSION_DEPTH:
        return ValidationResult(
            valid=False,
            error_code="H06",
            error_msg="ABORT: max recursion depth 64 exceeded — HALTING_PROBLEM guard",
            sentence=text
        )
    # ... existing logic continues
```

Windsurf instruction: find the validate() function signature in grammar.py,
add _depth parameter and the guard block at the top of the function body.

---

## TASK_1.3 — TAXONOMY UPGRADE — REFINEMENT_TYPE
### File: IMV/core/taxonomy.py
### Priority: [P1][I2] · Implication: wrong library claims pass without scalar check

Add REFINEMENT_TYPE constants and a check function:

```python
# Add to taxonomy.py

LIBRARY_SCALAR_MIN: dict[str, float] = {
    "COGNITIVO":  0.95,
    "TRUST":      0.92,
    "SAMU":       0.88,
    "CRYPTO":     0.88,
    "GATE":       0.82,
    "STACKING":   0.85,
    "WORK":       0.80,
    "SOCIAL":     0.80,
    "METHOD":     0.80,
    "ACTIVITY":   0.80,
}

LIBRARY_FOUNDATION_REQUIRED: dict[str, bool] = {
    "TRUST":    True,
    "COGNITIVO":True,
    "CRYPTO":   True,
    "GATE":     True,
    "SAMU":     False,
    "STACKING": False,
    "WORK":     False,
    "SOCIAL":   False,
    "METHOD":   False,
    "ACTIVITY": False,
}

def check_refinement_type(library: str, scalar: float, foundation_valid: bool) -> tuple[bool, str]:
    """
    REFINEMENT_TYPE check — DEPENDENT_TYPE enforcement per library.
    Returns (passes: bool, reason: str)
    """
    min_scalar = LIBRARY_SCALAR_MIN.get(library, 0.80)
    needs_foundation = LIBRARY_FOUNDATION_REQUIRED.get(library, False)

    if scalar < min_scalar:
        return False, f"SCALAR_BELOW_MIN: {library} requires S≥{min_scalar}, got S={scalar:.3f}"

    if needs_foundation and not foundation_valid:
        return False, f"FOUNDATION_INVALID: {library} requires [foundation] VALID"

    return True, f"REFINEMENT_TYPE OK: {library} S={scalar:.3f}"
```

Windsurf instruction: open IMV/core/taxonomy.py, add the three blocks above.
Then find where library validation happens in grammar.py or samu.py and
call check_refinement_type() before accepting a sentence.

---

## TASK_1.4 — ZERO_KNOWLEDGE_PROOF STUB → NOTARIA
### File: RUNTIME/RUNNERS/notaria.runner
### Priority: [P2][I2] · Implication: NOTARIA certifies without proof-of-existence

Add ZKP stub comment block at the top of notaria.runner:

```
*> NOTARIA ZKP STUB — ZERO_KNOWLEDGE_PROOF integration point
*> Status: STUB — implement in Phase 3 (QUANTUM_SEC axis)
*>
*> ZKP model for NOTARIA:
*>   PROVER:   document owner proves existence without revealing content
*>   VERIFIER: NOTARIA verifies the proof against H63 crystal hash
*>   PROTOCOL: hash(document) → commit → reveal(hash_only) → verify
*>
*> When implemented, replace STEP_3 in SAGA_NOTARIA with:
*>   STEP_3: verify ZKP_PROOF(document_hash) → certify if valid
*>   COMPENSATE: unseal if ZKP verification fails
```

---

## TEST FILE: IMV/tests/test_grammar_contracts.py
### Windsurf: create this file from scratch

```python
"""
test_grammar_contracts.py
Tests for TASK_1.1, TASK_1.2, TASK_1.3 — grammar contracts and refinement types.
[P1] Gate: all tests pass before Phase 2 begins.
"""
import pytest
from IMV.core.grammar import validate, MAX_RECURSION_DEPTH
from IMV.core.taxonomy import check_refinement_type, LIBRARY_SCALAR_MIN


def test_bnf_contract_present():
    """TASK_1.1: grammar.py module docstring contains BNF contract."""
    import IMV.core.grammar as g
    src = g.__doc__ or ""
    assert "SENTENCE" in src and "LIBRARY" in src and "BIND" in src


def test_max_recursion_constant():
    """TASK_1.2: MAX_RECURSION_DEPTH is defined and equals 64."""
    assert MAX_RECURSION_DEPTH == 64


def test_decidability_guard_triggers():
    """TASK_1.2: validate() returns ABORT when depth >= 64."""
    result = validate("TRUST FOUNDATION =><= verifica [scope] --[⊗] [term]", _depth=64)
    assert result.valid is False
    assert "H06" in str(result.error_code)


def test_refinement_type_trust_passes():
    """TASK_1.3: TRUST passes with S=0.93 and foundation valid."""
    ok, reason = check_refinement_type("TRUST", 0.93, foundation_valid=True)
    assert ok is True


def test_refinement_type_trust_fails_low_scalar():
    """TASK_1.3: TRUST fails with S=0.80 (below 0.92 minimum)."""
    ok, reason = check_refinement_type("TRUST", 0.80, foundation_valid=True)
    assert ok is False
    assert "SCALAR_BELOW_MIN" in reason


def test_refinement_type_trust_fails_no_foundation():
    """TASK_1.3: TRUST fails when foundation_valid=False."""
    ok, reason = check_refinement_type("TRUST", 0.95, foundation_valid=False)
    assert ok is False
    assert "FOUNDATION_INVALID" in reason


def test_refinement_type_work_passes_without_foundation():
    """TASK_1.3: WORK passes with S=0.82, foundation not required."""
    ok, reason = check_refinement_type("WORK", 0.82, foundation_valid=False)
    assert ok is True


def test_all_libraries_have_scalar_min():
    """TASK_1.3: all 9 libraries have a defined SCALAR_MIN."""
    libraries = ["TRUST","SAMU","CRYPTO","GATE","STACKING","WORK","SOCIAL","METHOD","ACTIVITY"]
    for lib in libraries:
        assert lib in LIBRARY_SCALAR_MIN, f"{lib} missing from LIBRARY_SCALAR_MIN"


def test_valid_lacho_sentence_still_passes():
    """Regression: valid sentence still validates after TASK_1.1-1.3 changes."""
    result = validate("TRUST FOUNDATION =><= verifica [scope] --[As de Guía] [term]")
    assert result.valid is True
```
