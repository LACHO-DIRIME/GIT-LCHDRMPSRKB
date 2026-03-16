#!/bin/bash
# tools/github_sync.sh · DIRIME/IMV · Sovereign Git Sync
# Invocado por: macro_components.lacho → macro_cierre
# [term] :: activo · [seal of secrecy] :: activo

set -euo pipefail
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
DB_SRC="FOLDERS NO RAG INPUT/ELPULSAR LOCAL/$$DIA.CORPUS_NOTARIA_KALIL.MU-STORE.db"
[ -f "$DB_SRC" ] && git add "$DB_SRC"

# ── STAGE 3: Nerve Cells del día ───────────────────────────────────────────
git add "FOLDERS NO RAG INPUT/ELPULSAR LOCAL/$$DIA."*.txt 2>/dev/null || true

# ── STAGE 4: IMV core si hay cambios ───────────────────────────────────────
git add IMV/core/ledger.py IMV/core/grammar.py IMV/interface/chat.py 2>/dev/null || true
git add IMV/tools/github_sync.sh 2>/dev/null || true

# ── STAGE 5: LACHO_FILES ───────────────────────────────────────────────────
git add "FOLDERS NO RAG INPUT/LACHO_FILES/micro_solutions.lacho" 2>/dev/null || true
git add "FOLDERS NO RAG INPUT/LACHO_FILES/notaria_endpoints.lacho" 2>/dev/null || true

# ── COMMIT con formato COMMIT_LACHO ────────────────────────────────────────
TX=$(python3 "$REPO_ROOT/IMV/main.py" --tx-count 2>/dev/null || echo "1335")
SCALAR=$(python3 "$REPO_ROOT/IMV/main.py" --scalar 2>/dev/null || echo "0.78")
CRISTALES=$(python3 "$REPO_ROOT/IMV/main.py" --crystals 2>/dev/null || echo "42")

MSG="STACKING UF[H63] :: cristaliza :: notaria_$FECHA --[NdO] [term]
TX=$TX · cristales=$CRISTALES · S=$SCALAR · H63 既濟 · $$DIA $FECHA"

git diff --cached --quiet && echo "Nada que commitear." && exit 0

git commit -m "$MSG"
git push origin main

echo "✅ github_sync.sh · commit notarial completo · $$DIA $FECHA · [term]"
