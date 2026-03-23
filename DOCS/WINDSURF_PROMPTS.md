# DOCS/WINDSURF_PROMPTS.md
# Copy-paste prompts for Windsurf Cascade — one per task
# Replace [CURRENT_SCALAR] and [TERM] with actual values each session

---

## PROMPT: BACKUP FIRST (always)

```
Run this in terminal before touching any file:
bash MAINTENANCE/backup.sh
Confirm the output ends with "=== BACKUP COMPLETE ===" before proceeding.
```

---

## PROMPT: TASK_1.1 — Grammar Formalization

```
Open: IMV/core/grammar.py
Find: the module docstring (first triple-quoted string at the top of the file).
After the closing triple-quote of the docstring, insert this exact text as a new docstring block:

"""
LACHO FORMAL GRAMMAR — BNF CONTRACT v1.0
Context-sensitive (Chomsky N3)

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
ENCODING: UTF-8, CJK block U+4E00-U+9FFF supported
"""

Then add this constant near the top of the module (after imports):
MAX_RECURSION_DEPTH = 64

Run: python3 -c "import IMV.core.grammar; print('OK')"
Confirm: no import errors.
```

---

## PROMPT: TASK_1.2 — Decidability Guard

```
Open: IMV/core/grammar.py
Find: the validate() function definition.
Add _depth: int = 0 as the last parameter.
Add these lines as the FIRST two lines inside the function body:

    if _depth >= MAX_RECURSION_DEPTH:
        return ValidationResult(valid=False, error_code="H06",
            error_msg="ABORT: max recursion depth 64 exceeded")

Run: pytest IMV/tests/test_grammar_contracts.py::test_decidability_guard_triggers -v
Confirm: 1 passed.
```

---

## PROMPT: TASK_1.3 — Taxonomy Upgrade

```
Open: IMV/core/taxonomy.py
Add at the END of the file (before any if __name__ == "__main__" block):

LIBRARY_SCALAR_MIN: dict[str, float] = {
    "COGNITIVO":  0.95, "TRUST": 0.92,
    "SAMU": 0.88, "CRYPTO": 0.88, "GATE": 0.82,
    "STACKING": 0.85, "WORK": 0.80, "SOCIAL": 0.80,
    "METHOD": 0.80, "ACTIVITY": 0.80,
}

LIBRARY_FOUNDATION_REQUIRED: dict[str, bool] = {
    "TRUST": True, "COGNITIVO": True, "CRYPTO": True, "GATE": True,
    "SAMU": False, "STACKING": False, "WORK": False,
    "SOCIAL": False, "METHOD": False, "ACTIVITY": False,
}

def check_refinement_type(library: str, scalar: float, foundation_valid: bool) -> tuple[bool, str]:
    min_scalar = LIBRARY_SCALAR_MIN.get(library, 0.80)
    needs_foundation = LIBRARY_FOUNDATION_REQUIRED.get(library, False)
    if scalar < min_scalar:
        return False, f"SCALAR_BELOW_MIN: {library} requires S>={min_scalar}, got S={scalar:.3f}"
    if needs_foundation and not foundation_valid:
        return False, f"FOUNDATION_INVALID: {library} requires [foundation] VALID"
    return True, f"REFINEMENT_TYPE OK: {library} S={scalar:.3f}"

Run: pytest IMV/tests/test_grammar_contracts.py -v
Confirm: 9/9 passed.
```

---

## PROMPT: TASK_2.1 — Hexagonal Ports

```
Create new file: IMV/core/ports.py
Paste the COMPLETE content from TASKS/PHASE2_ARCHITECTURE.md,
section "### IMV/core/ports.py — create this file:"

Create new file: IMV/adapters/cli_adapter.py
Paste content from section "### IMV/adapters/cli_adapter.py"

Create new file: IMV/adapters/groq_adapter.py
Paste content from section "### IMV/adapters/groq_adapter.py"

Create new file: IMV/adapters/db_adapter.py
Paste content from section "### IMV/adapters/db_adapter.py"

Run: python3 -c "from IMV.core.ports import PORTS, SentencePort; print('ports OK')"
Run: python3 -c "from IMV.adapters.cli_adapter import CLISentenceAdapter; print('cli adapter OK')"
Confirm: no import errors.
```

---

## PROMPT: TASK_2.2 — Library Isolation

```
Create the following 5 files with content from TASKS/PHASE2_ARCHITECTURE.md
section "TASK_2.2":

  IMV/libraries/trust_context.py
  IMV/libraries/stacking_context.py
  IMV/libraries/crypto_context.py
  IMV/libraries/gate_context.py
  IMV/libraries/samu_context.py

Run: python3 -c "
from IMV.libraries.trust_context import LIBRARY_NAME, SCALAR_MIN
from IMV.libraries.gate_context import ABORT_CODES
print(f'TRUST: {LIBRARY_NAME} S>={SCALAR_MIN}')
print(f'GATE abort codes: {ABORT_CODES}')
print('library contexts OK')
"
Confirm: output shows correct values.
```

---

## PROMPT: DIRECTORY MIGRATION

```
Run each command in terminal, in order.
After each mv command, verify the source is gone and target exists.

Step 1 — Create new directories:
mkdir -p CORPUS/GLOSSARY CORPUS/MICRO CORPUS/DOCS CORPUS/DRA CORPUS/PRACTICE
mkdir -p RUNTIME/AGENTS RUNTIME/THEATER RUNTIME/RUNNERS RUNTIME/DASHBOARDS RUNTIME/CONFIG
mkdir -p RUNTIME/NERVE_CELLS/{mon,tue,wed,thu,fri,sat,sun}
mkdir -p RUNTIME/PROGRAMS/{DSL,CHINA,NOTARIA,EXTENSIONS}
mkdir -p IMV/adapters IMV/libraries IMV/data
mkdir -p CAPA_B CAPA_C CONTROL TASKS

Step 2 — Move (check each):
[paste each mv command from TASKS/MIGRATION.md STEP_2 one at a time]

Step 3 — After all moves:
grep -r "FOLDERS NO RAG" IMV/
# Must return: zero matches
# If matches found: fix them before continuing

Step 4 — Verify:
pytest IMV/tests/ -v
python3 IMV/main.py --stats
# Both must work without errors
```

---

## PROMPT: LANGUAGE PURITY (DIRECTIVE 1)

```
Open each file listed in CONTROL/language_purity.md
Apply the find-and-replace pairs listed under "REFACTOR MAP"
Do NOT change string literals that are LACHO data (knot names, library names)

After all replacements, run:
grep -rn "# [a-záéíóúñ]" IMV/core/
# Expected: zero matches or only data strings

Run: pytest IMV/tests/ -v
Confirm: same pass rate as before purity changes.
```
