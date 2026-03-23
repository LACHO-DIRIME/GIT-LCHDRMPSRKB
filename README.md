# DIRIME — SOVEREIGN UPGRADE PACKAGE
## V0.3.0 → V0.4.0 · Sovereign Integration Guide
## Generated: 2026-03-22 · Based on: lacho_final_prompting.txt

---

## WHAT THIS PACKAGE IS

This directory is the **deliverable scaffold** for the DIRIME/LACHO upgrade.
It contains:
- The new directory structure (DIRECTIVE 2)
- All SPEC files your Windsurf AI needs to generate code
- Migration scripts to apply to your existing DIRIME project
- Session protocols for Windsurf + Claude + Gemini tripartite work
- Priority conventions for every task

It does NOT contain your existing code.
Your Windsurf AI will generate new code INTO this skeleton,
then you migrate existing files using the scripts in TASKS/MIGRATION.md.

---

## PRIORITY CONVENTION (my own — used throughout all files)

```
[P0]  BLOCKER      — must execute BEFORE anything else · risk: total loss
[P1]  CRITICAL     — breaks functionality if skipped · do this week
[P2]  HIGH         — closes a confirmed gap · do this sprint
[P3]  MEDIUM       — improves quality/performance · schedule it
[P4]  LOW          — enhancement · nice to have
[P5]  DEFERRED     — Phase 3+ or hardware-dependent · do not touch now

IMPLICATION LEVELS (how much breaks if ignored):
[I1]  SYSTEMIC     — entire IMV fails or corrupts data
[I2]  FUNCTIONAL   — one module fails silently
[I3]  DEGRADED     — works but slower or with errors
[I4]  COSMETIC     — works fine, just harder to maintain
```

---

## PHASE MAP — 4 WEEKS · 5h/day

```
WEEK 1
  Day 0   [P0][I1] BACKUP_PROTOCOL         → before touching anything
  Day 1   [P0][I1] FOUNDATION_AUDIT        → gate: S≥0.80, 49/49 tests
  Day 2   [P1][I2] GRAMMAR_FORMALIZATION   → TASK_1.1 + TASK_1.2
  Day 3   [P1][I2] TAXONOMY_UPGRADE        → TASK_1.3 (REFINEMENT_TYPE)
  Day 4   [P1][I1] HEXAGONAL_PORTS         → TASK_2.1 (ports.py + adapters/)
  Day 5   [P1][I2] LIBRARY_ISOLATION       → TASK_2.2 (libraries/ contexts)

WEEK 2
  Day 1   [P1][I1] DIRECTORY_MIGRATION     → DIRECTIVE 2 full execution
  Day 2   [P2][I2] EVENT_SOURCING          → TASK_2.3 (ledger.py upgrade)
  Day 3   [P2][I2] CIRCUIT_BREAKER         → TASK_2.4 (groq/bridge.py)
  Day 4   [P2][I2] MONAD_CHAINING          → TASK_3.1 (foundation.py)
  Day 5   [P2][I3] RAG_INCREMENTAL         → TASK_3.2 + TASK_3.4 (rag.py)

WEEK 3
  Day 1   [P2][I2] ALGEBRAIC_EFFECTS       → TASK_3.3 (samu.py isolation)
  Day 2   [P2][I2] DEPENDENT_CONTRACTS     → TASK_3.5 (grammar.py contracts)
  Day 3   [P1][I1] SOVEREIGN_DB_MIGRATION  → APP_1 (5x capacity)
  Day 4   [P2][I2] VECTOR_RAG              → APP_7 (FAISS index)
  Day 5   [P2][I2] STREAMING_VALIDATOR     → APP_3 + APP_8

WEEK 4
  Day 1   [P2][I2] ASYNC_SAMU             → APP_5 + APP_6 (batch crystal)
  Day 2   [P2][I2] SHARDED_LEDGER         → APP_4 (5 domain shards)
  Day 3   [P3][I3] CLOUD_CI               → CLOUD_1 GitHub Actions
  Day 4   [P3][I3] CLOUD_ENDPOINTS        → CLOUD_2 Cloudflare + CLOUD_3 Supabase
  Day 5   [P2][I1] SCALAR_LADDER_CHECK    → target S≥0.92 · cristales≥80
```

---

## GAP CLOSURE MAP

```
GAP_1 GRAMMAR_INFORMAL     → TASK_1.1  [P1][I2]  Week 1 Day 2
GAP_2 SCALAR_VOLATILITY    → APP_15+CLOUD_1+CLOUD_4  [P1][I1]  Week 3-4
GAP_3 LEDGER_SNAPSHOT_ONLY → TASK_2.3  [P2][I2]  Week 2 Day 2
GAP_4 TIGHT_COUPLING       → TASK_2.1  [P1][I1]  Week 1 Day 4
GAP_5 RAG_FULL_REBUILD      → TASK_3.4  [P2][I3]  Week 2 Day 5
GAP_6 NO_CIRCUIT_BREAKER   → TASK_2.4  [P2][I2]  Week 2 Day 3
GAP_7 NOTARIA_NO_COMP      → TASK_2.5  [P2][I2]  Week 2 Day 3
GAP_8 LOCAL_ONLY_INFRA     → CLOUD_1-4  [P3][I3]  Week 4
GAP_9 GLOSSARY_MANUAL      → APP_13+GLOSSARY_JSON  [P2][I2]  Week 3
GAP_10 HARDWARE (accepted) → CLOUD_5 partial mitigation only
```

---

## SCALAR S TARGET LADDER

```
Start of Week 1:  S = current  · cristales = current
End of Week 1:    S ≥ 0.83     · cristales ≥ 62
End of Week 2:    S ≥ 0.86     · cristales ≥ 66
End of Week 3:    S ≥ 0.89     · cristales ≥ 72
End of Week 4:    S ≥ 0.92     · cristales ≥ 80
                  V0.4.0 TAGGED · all 9 gaps CLOSED
```

---

## TRIPARTITE ROLES (adapted — Claude replaces Gemini's stress-test role here)

```
WINDSURF CASCADE  → file system · terminal · git · code generation · tests
CLAUDE            → architecture design · contracts · audit · this package
GEMINI            → stress testing · edge cases · external doc cross-check

HANDOFF:
  Claude writes SPEC → Windsurf implements → Claude audits diff
  Windsurf produces diff → Gemini stress tests → Windsurf fixes
  Operator is the integration point — not any AI
```

---

## DIRECTORY NAMING RULES (DIRECTIVE 2)

```
UPPER_CASE  top-level sovereign dirs:  CORPUS · RUNTIME · CONTROL · TASKS
lower_case  technical subdirs:         core/ · adapters/ · config/ · data/
Mixed       proper names/identifiers:  BIBLIA · COGNITIVO · THEATER · AGENTS

NEVER:
  spaces in names          "FOLDERS NO RAG INPUT" → RUNTIME
  version suffixes         DIRIME_v2 → CAPA_B
  date directories         2026-03-18_corrections → corrections/
  "copiar" or "copy"       AUX21-03-copiar2 → ARCHIVE
  parentheses              TOMO(A) → TOMO_A
```
