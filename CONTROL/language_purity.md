# CONTROL/language_purity.md
# DIRECTIVE 1 — LANGUAGE PURITY IN LACHO CODE
# [P1][I4] Apply to all IMV/core/*.py files
# WHO: Windsurf applies · Claude verifies

---

## THE RULE

ALLOWED Spanish:
  - String literals that ARE data (operator-typed names, LACHO knot names)
  - JOURNAL/*.md files (session notes)
  - git commit messages (operator writes them)
  - .theater and .gate file comments (orchestration scripts)

NOT ALLOWED Spanish:
  - Variable names
  - Function names
  - Class names
  - Module docstrings
  - Inline code comments
  - Enum member names
  - Exception class names
  - Type aliases
  - Config keys in JSON/YAML
  - Test function names
  - Log messages emitted by the system

BORDER CASE:
  ALLOWED:     name = "FUNDAMENTOS DEL LENGUAJE"  ← it is data
  ALLOWED:     label = "As de Guía"               ← it is data (LACHO knot name)
  NOT ALLOWED: # verifica condiciones soberanas   ← it is code comment
  NOT ALLOWED: def verificar_condiciones():       ← it is code
  NOT ALLOWED: estado = "activo"                  ← it is a code variable
  CORRECT:     state = "ACTIVE"                   ← enum value

---

## REFACTOR MAP — files to fix

### IMV/core/grammar.py
Windsurf: find and replace in this file:

  COMMENT: "# verifica el orden de 6 elementos"
  REPLACE:  "# validates 6-slot sentence order"

  COMMENT: "# mapea el estado AST"
  REPLACE:  "# maps AST state to hexagram"

  COMMENT: "# Detecta si el texto contiene"
  REPLACE:  "# detects CJK characters in text"

### IMV/core/samu.py
Windsurf: find and replace:

  "DELIBERANDO"    → "DELIBERATING"
  "RESOLVIENDO"    → "RESOLVING"
  "SAMU APRUEBA"   → "SAMU_APPROVED"
  "Tardanza deliberada activada" → "DELIBERATE_DELAY_ACTIVE"

### IMV/core/foundation.py
Windsurf: find and replace in docstrings:
  All Spanish prose in module docstring → translate to English
  "comprometido"   → "COMPROMISED"

### IMV/core/ledger.py
Windsurf: find and replace:
  "registro soberano"         → "sovereign ledger"
  All f-string messages with Spanish → translate to English

### IMV/core/rag.py
Windsurf: find and replace:
  "Encuentra ejemplos soberanos" → "retrieves sovereign examples"
  All Spanish in docstrings → translate to English

---

## NAMING CONVENTION (apply to all new code)

```
Classes:    PascalCase     SovereignLedger · GrammarValidator · CircuitBreaker
Functions:  snake_case     validate_sentence() · emit_crystal() · check_effect()
Constants:  UPPER_CASE     SCALAR_MIN · ABORT_HEXAGRAM · MAX_RECURSION_DEPTH
Enums:      PascalCase class, UPPER_CASE members
              class LibraryType(Enum):
                  TRUST    = "TRUST"
                  STACKING = "STACKING"
Files:      snake_case.py  grammar_patch_kalil.py · ports.py
Config:     UPPER_CASE keys  { "SCALAR_MIN": 0.88 }
Log format: [TIMESTAMP] [LIBRARY] [EVENT] [SCALAR] [UF]
              2026-03-22 TRUST CRYSTAL_WRITTEN S=0.80 H63
```

---

## VERIFICATION COMMAND
After applying all replacements, Windsurf run:

```bash
# Check for Spanish in code comments (not in strings)
grep -rn "# [a-záéíóúñ]" IMV/core/ | grep -v "\.pyc"

# Check for Spanish variable names (rough check)
grep -rn "def [a-z]*[áéíóúñ]" IMV/core/

# Check for Spanish in log messages
grep -rn 'print\(.*[áéíóúñ]' IMV/core/
grep -rn 'logger\.\w\+(.*[áéíóúñ]' IMV/core/
```

Expected result: zero matches (or only data strings, which are allowed).
