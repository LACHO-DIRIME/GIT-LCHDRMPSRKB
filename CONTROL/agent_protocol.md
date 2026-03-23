# CONTROL/agent_protocol.md
# TRIPARTITE CONTRACT — Windsurf · Claude · Gemini
# [P0][I4] Write once, follow always

---

## WINDSURF CASCADE

OWNS:  file system · terminal · git · test execution · code generation
DOES:  writes code · runs scripts · commits · migrates directories
       executes pytest · applies diffs · installs dependencies
DOES NOT: design architecture · choose between patterns · decide trade-offs

INPUT format:
  "Open FILE at LINE N. Add/replace/remove EXACT_CODE. Run COMMAND to verify."
  Always include: file path + action + verification command

OUTPUT format:
  diff or terminal output pasted back to Claude for audit

WINDSURF SESSION START RITUAL (5 min):
  1. Read JOURNAL/ACTIVE/SESION_ACTIVA.md
  2. Run: python3 IMV/main.py --stats → note S value
  3. Run: pytest IMV/tests/ -v → confirm tests passing
  4. Open today's task from TASKS/ (current phase)
  5. Confirm gate from previous session is met before starting

WINDSURF COMMIT FORMAT:
  "STACKING UF[H63] :: crystallizes :: [task_name] --[⊗] [term]"

---

## CLAUDE (this chat)

OWNS:  architecture design · contracts · integration · audit · this package
DOES:  designs module boundaries · writes SPEC files · reviews diffs
       catches semantic violations of LACHO principles
       generates migration scripts and task files like this one
       audits Windsurf diffs before each commit
DOES NOT: execute terminal commands · access filesystem directly
           write production code that goes into IMV/core/

INPUT format:
  "Here is the diff from Windsurf. Audit against [TASK_N.N]."
  "Design the interface for [module]. Windsurf will implement."
  "Gap [GAP_N] is still open. What is the minimal fix?"

OUTPUT format:
  structured decision with rationale, or SPEC file content

CLAUDE AUDIT CHECKLIST (per diff):
  [ ] English-only variable/function/class names?
  [ ] No FOLDERS NO RAG INPUT path references?
  [ ] No tight coupling (direct imports between grammar/samu/ledger)?
  [ ] Test coverage added for new code?
  [ ] CONV naming convention followed (DOMAIN_LAYER_TERM)?
  [ ] Scalar S would not decrease from this change?

---

## GEMINI

OWNS:  stress testing · edge case generation · external validation
DOES:  generates 10-20 test cases per feature after Windsurf implements
       cross-checks against external documentation
       challenges design decisions with counter-examples
       tests LACHO sentences for edge cases at scale (10,000 sentences)
DOES NOT: write production code · commit anything · design architecture

INPUT format:
  "Given this implementation [paste code], find failure modes.
   Focus on: [specific concern]. Generate numbered test cases."

OUTPUT format:
  numbered list of test cases with expected behavior

GEMINI STRESS TEST SESSIONS:
  Use Groq endpoint_2 (GLOSSARY_TERM → IMV_MODULE routing) as oracle
  Run on $sat (backup day) — never during primary 5h sessions
  Export results as JSON → paste to Claude for gap analysis

---

## HANDOFF PROTOCOL

```
Claude designs SPEC
  ↓
Windsurf implements from SPEC
  ↓
Windsurf pastes diff to Claude
  ↓
Claude audits diff against checklist
  ↓
Claude approves → Windsurf commits
  ↓
After commit: paste feature to Gemini
  ↓
Gemini generates stress test cases
  ↓
Windsurf implements fixes from Gemini gaps
  ↓
Repeat until Gemini finds zero critical gaps
```

## SESSION RULES

- One AI owns one domain per task — never split a task between two AIs
- Never ask the same question to two AIs simultaneously
- The operator is the integration point — not any AI
- If blocked → document in JOURNAL/ACTIVE/PENDIENTES.md and switch task
- At session end → update SESION_ACTIVA.md with S value and progress

---

## PRIORITY CONVENTION (quick ref)

```
[P0][I1]  BLOCKER + SYSTEMIC   → execute immediately, nothing else first
[P0][I4]  BLOCKER + COSMETIC   → execute first session, low risk
[P1][I1]  CRITICAL + SYSTEMIC  → this week, no exceptions
[P1][I2]  CRITICAL + FUNCTIONAL → this week
[P2][I2]  HIGH + FUNCTIONAL    → this sprint
[P2][I3]  HIGH + DEGRADED      → this sprint, can defer 1 day
[P3][I3]  MEDIUM + DEGRADED    → schedule, not urgent
[P4][I4]  LOW + COSMETIC       → nice to have
[P5]      DEFERRED             → Phase 3+ or hardware-dependent
```
