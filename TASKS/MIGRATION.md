# TASKS/MIGRATION.md
# [P0][I1] Directory Migration — DIRECTIVE 2 Full Execution
# Execute in WINDSURF terminal · steps are ordered · do not reorder

---

## STEP_0 — AUDIT (gate before migration)

```bash
# Run from DIRIME/ root
cd /path/to/DIRIME

# 0.1 Backup first (mandatory)
bash MAINTENANCE/backup.sh
# GATE: backup.log shows BACKUP_OK before continuing

# 0.2 Test suite baseline
pytest IMV/tests/ -v
# GATE: must show passing tests before migration
# If tests fail → fix tests before migration, not after

# 0.3 Current scalar
python3 IMV/main.py --stats
# GATE: note S value and TX count — compare after migration

# 0.4 Current file count
find . -type f | wc -l
find . -type d | wc -l
# Note these numbers for comparison after migration
```

---

## STEP_1 — CREATE NEW SKELETON

```bash
# Run from DIRIME/ root
# These are the new directories that do not exist yet

mkdir -p CORPUS/GLOSSARY
mkdir -p CORPUS/MICRO
mkdir -p CORPUS/DOCS
mkdir -p CORPUS/DRA
mkdir -p CORPUS/PRACTICE

mkdir -p RUNTIME/AGENTS
mkdir -p RUNTIME/NERVE_CELLS/{mon,tue,wed,thu,fri,sat,sun}
mkdir -p RUNTIME/PROGRAMS/DSL
mkdir -p RUNTIME/PROGRAMS/CHINA
mkdir -p RUNTIME/PROGRAMS/NOTARIA
mkdir -p RUNTIME/PROGRAMS/EXTENSIONS
mkdir -p RUNTIME/THEATER
mkdir -p RUNTIME/RUNNERS
mkdir -p RUNTIME/DASHBOARDS
mkdir -p RUNTIME/CONFIG

mkdir -p IMV/adapters
mkdir -p IMV/libraries
mkdir -p IMV/data

mkdir -p CAPA_B
mkdir -p CAPA_C
mkdir -p CONTROL
mkdir -p TASKS
```

---

## STEP_2 — MOVE FILES (mv, not cp — preserve git history)

```bash
# 2.1 Rename CORPUS subdirectories
mv CORPUS/COGNITIVO_FRAMEWORK CORPUS/COGNITIVO   2>/dev/null || true
mv CORPUS/MICRO_ARCHITECTURE CORPUS/MICRO         2>/dev/null || true
mv CORPUS/DOCUMENTATION CORPUS/DOCS               2>/dev/null || true
mv CORPUS/DYNAMIC_RESOURCE_ALLOCATION CORPUS/DRA  2>/dev/null || true
mv CORPUS/PRACTICE_IMPLEMENTATIONS CORPUS/PRACTICE 2>/dev/null || true

# 2.2 Move LACHO_FILES → CONTROL
mv LACHO_FILES/* CONTROL/ 2>/dev/null || true

# 2.3 Move version dirs → CAPA names
mv DIRIME_v2/* CAPA_B/ 2>/dev/null || true
mv DIRIME_v3/* CAPA_C/ 2>/dev/null || true

# 2.4 Move tools → IMV/tools
mv tools/* IMV/tools/ 2>/dev/null || true

# 2.5 Rename FOLDERS NO RAG INPUT → RUNTIME
# NOTE: quotes required due to spaces in name
mv "FOLDERS NO RAG INPUT/AGENTS/"* RUNTIME/AGENTS/ 2>/dev/null || true
mv "FOLDERS NO RAG INPUT/ELPULSAR LOCAL/"* RUNTIME/NERVE_CELLS/ 2>/dev/null || true
mv "FOLDERS NO RAG INPUT/UNICODE/PROGRAMS/"* RUNTIME/PROGRAMS/ 2>/dev/null || true
mv "FOLDERS NO RAG INPUT/THEATER/"* RUNTIME/THEATER/ 2>/dev/null || true
mv "FOLDERS NO RAG INPUT/RUNNERS/"* RUNTIME/RUNNERS/ 2>/dev/null || true
mv "FOLDERS NO RAG INPUT/DASHBOARD_INTERFACES/"* RUNTIME/DASHBOARDS/ 2>/dev/null || true
mv "FOLDERS NO RAG INPUT/CONFIG_FILES/"* RUNTIME/CONFIG/ 2>/dev/null || true

# 2.6 Move sovereign.db → IMV/data/
mv sovereign.db IMV/data/ 2>/dev/null || true
mv sovereign.db.backup IMV/data/ 2>/dev/null || true

# 2.7 Consolidate all glossary .index.lacho files
find . -name "*.index.lacho" -not -path "./CORPUS/GLOSSARY/*" \
  -exec mv {} CORPUS/GLOSSARY/ \; 2>/dev/null || true
```

---

## STEP_3 — CONSOLIDATE DUPLICATES

```bash
# 3.1 Verify DRA content before deleting duplicate
diff -r CORPUS/DRA "CORPUS/AUX21-03-copiar2/DYNAMIC_RESOURCE_ALLOCATION" 2>/dev/null
# If diff shows only minor differences → review manually before rm
# If diff is empty (identical) → safe to remove:
rm -rf CORPUS/AUX21-03-copiar2

# 3.2 Remove FOLDERS NO RAG INPUT (now empty after STEP_2)
rm -rf "FOLDERS NO RAG INPUT/UNICODE/DYNAMIC_RESOURCE_ALLOCATION" 2>/dev/null || true
rm -rf "FOLDERS NO RAG INPUT/LACHO_FILES" 2>/dev/null || true
# After verifying all moves completed:
rm -rf "FOLDERS NO RAG INPUT" 2>/dev/null || true

# 3.3 Remove remaining empty dirs
rm -rf DIRIME_v2 DIRIME_v3 LACHO_FILES tools 2>/dev/null || true
rm -rf GH_ROOT IMAGENES "INBOX(gradient)" GENERATED 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true
```

---

## STEP_4 — MERGE LOGS INTO TASKS/

```bash
# 4.1 Create TASKS/ files
cat UPGRADE_TASKING/01_TAREAS_INMEDIATAS/*.md > TASKS/IMMEDIATE.md 2>/dev/null || true
cat UPGRADE_TASKING/02_TAREAS_DESARROLLO/*.md > TASKS/DEVELOPMENT.md 2>/dev/null || true
cat UPGRADE_TASKING/03_TAREAS_PLANIFICACION/*.md > TASKS/PLANNING.md 2>/dev/null || true
cat UPGRADE_TASKING/04_PLANES_HISTORICOS/*.md > TASKS/HISTORY.md 2>/dev/null || true

# 4.2 Merge 35 session logs into single file
cat UPGRADE_TASKING/07_REGISTROS_MANTENIMIENTO/**/*.txt >> TASKS/MAINTENANCE_LOG.md 2>/dev/null || true

# 4.3 Remove UPGRADE_TASKING (after verifying TASKS/ is complete)
rm -rf UPGRADE_TASKING 2>/dev/null || true
```

---

## STEP_5 — UPDATE PYTHON PATH CONSTANTS

```bash
# These are the exact strings to find and replace in IMV/core/rag.py
# WINDSURF: open each file and apply replacements

# IMV/core/rag.py — path constants
# OLD:  "FOLDERS NO RAG INPUT" / "THEATER"
# NEW:  "RUNTIME" / "THEATER"
#
# OLD:  "FOLDERS NO RAG INPUT" / "RUNNERS"
# NEW:  "RUNTIME" / "RUNNERS"
#
# OLD:  "FOLDERS NO RAG INPUT" / "AGENTS"
# NEW:  "RUNTIME" / "AGENTS"
#
# OLD:  "FOLDERS NO RAG INPUT" / "ELPULSAR LOCAL"
# NEW:  "RUNTIME" / "NERVE_CELLS"
#
# OLD:  sovereign.db  (root path)
# NEW:  IMV/data/sovereign.db

# IMV/main.py — any hardcoded paths
grep -n "FOLDERS NO RAG\|LACHO_FILES\|DIRIME_v2\|DIRIME_v3\|sovereign.db" IMV/main.py
# Fix each occurrence found

# IMV/core/language_routing.py
grep -n "FOLDERS NO RAG\|LACHO_FILES" IMV/core/language_routing.py

# Run after all replacements:
grep -r "FOLDERS NO RAG" IMV/
# GATE: zero matches
```

---

## STEP_6 — VERIFY

```bash
# 6.1 Tests still pass
pytest IMV/tests/ -v
# GATE: same number of passing tests as STEP_0

# 6.2 Main entry point works
python3 IMV/main.py --stats
# GATE: shows S value and TX count (same as STEP_0)

# 6.3 No broken path references
python3 -c "from IMV.core.grammar import validate; print('grammar OK')"
python3 -c "from IMV.core.rag import IMEBM25; print('rag OK')"
python3 -c "from IMV.core.ledger import SovereignLedger; print('ledger OK')"

# 6.4 sovereign.db accessible
python3 -c "import sqlite3; sqlite3.connect('IMV/data/sovereign.db').execute('PRAGMA integrity_check').fetchone()"

# 6.5 File count comparison
find . -type f | wc -l
# Should be significantly less than STEP_0 baseline
```

---

## STEP_7 — COMMIT

```bash
git add -A
git status
# Review all changes carefully before committing

git commit -m "STACKING UF[H63] :: crystallizes :: directory_redesign --[⊗] [term]"
```

---

## AFTER MIGRATION — proceed to TASKS/PHASE1_GRAMMAR.md
