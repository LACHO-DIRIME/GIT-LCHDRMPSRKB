#!/bin/bash
# tools/github_sync.sh · DIRIME/IMV · Sovereign Git Sync
# Invocado por: macro_components.lacho → macro_cierre
# [term] :: activo · [seal of secrecy] :: activo

set -euo pipefail

# ── FLAGS ──────────────────────────────────────────────────────────────────
WITH_ASKS=false
for arg in "$@"; do
  case $arg in
    --asks) WITH_ASKS=true ;;
  esac
done
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FECHA=$(date +"%d-%m")
DIA=$(date +"%a" | tr '[:upper:]' '[:lower:]')  # mon/tue/wed/thu/fri/sat/sun

cd "$REPO_ROOT"

# ── STAGE 1: Archivos NOTARIA ──────────────────────────────────────────────
git add "CORPUS/UNICODE PROGRAMS/UNICODE_NOTARIA"*.txt 2>/dev/null || true
git add "CORPUS/UNICODE PROGRAMS/UNICODE_NORA_NOTARIA.txt" 2>/dev/null || true
git add "CORPUS/UNICODE PROGRAMS/UNICODE_CARILO_NOTARIA.txt" 2>/dev/null || true
git add "CORPUS/UNICODE PROGRAMS/UNICODE_IMV_4NEURONAS_NOTARIA_V1.txt" 2>/dev/null || true

# ── STAGE 2: MU-STORE DB backup ────────────────────────────────────────────
DB_SRC="RUNTIME/NERVE_CELLS/$DIA.CORPUS_NOTARIA_KALIL.MU-STORE.db"
[ -f "$DB_SRC" ] && git add "$DB_SRC"

# ── STAGE 3: Nerve Cells del día ───────────────────────────────────────────
git add "RUNTIME/NERVE_CELLS/$DIA."*.txt 2>/dev/null || true

# ── STAGE 4: IMV core si hay cambios ───────────────────────────────────────
git add IMV/core/ledger.py IMV/core/grammar.py IMV/interface/chat.py 2>/dev/null || true
git add IMV/tools/github_sync.sh 2>/dev/null || true

# ── STAGE 5: LACHO_FILES ───────────────────────────────────────────────────
git add "CONTROL/micro_solutions.lacho" 2>/dev/null || true
git add "CONTROL/notaria_endpoints.lacho" 2>/dev/null || true

# ── STAGE 6: LEARNING/ y JOURNAL/ actualizados ────────────────────────────
git add LEARNING/*.md 2>/dev/null || true
git add JOURNAL/ALMANAQUE_SOBERANO.md 2>/dev/null || true
git add JOURNAL/LOG_PERMANENTE.md 2>/dev/null || true
git add JOURNAL/SESION_ACTIVA.md 2>/dev/null || true

# ── STAGE 7: Asks del día (si --asks flag activo) ─────────────────────────
if [ "$WITH_ASKS" = true ]; then
  ASKS_DIR="$REPO_ROOT/Askings for autoresearching by technical horizons"
  if [ -d "$ASKS_DIR" ]; then
    git add "$ASKS_DIR"/*.txt 2>/dev/null || true
    git add "$ASKS_DIR"/*.json 2>/dev/null || true
    git add "$ASKS_DIR"/*.yml 2>/dev/null || true
    echo "  📋 Asks del día incluidos en commit"
  fi
fi

# ── COMMIT con formato COMMIT_LACHO ────────────────────────────────────────
STATS=$(cd "$REPO_ROOT/IMV" && python3 -c "
from core.ledger import get_stats
from core.samu import get_scalar_s
import sys; sys.path.insert(0,'.')
s=get_stats()
print(s.get('transactions_total',0), s.get('crystals_total',0), get_scalar_s())
" 2>/dev/null || echo "0 0 0.0")
TX=$(echo $STATS | awk '{print $1}')
CRISTALES=$(echo $STATS | awk '{print $2}')
SCALAR=$(echo $STATS | awk '{print $3}')

MSG="STACKING UF[H63] :: cristaliza :: notaria_$FECHA --[NdO] [term]
TX=$TX · cristales=$CRISTALES · S=$SCALAR · H63 既濟 · $DIA $FECHA"

git diff --cached --quiet && echo "Nada que commitear." && exit 0

git commit -m "$MSG"
git push origin main

echo "✅ github_sync.sh · TX=$TX · S=$SCALAR · $DIA $FECHA"
