#!/bin/bash
# github_sync.sh · Suite Soberana · [term] :: activo
DIRIME_PATH="/media/Personal/PLANERAI/DIRIME"
DATE=$(date +"%Y-%m-%d %H:%M")
echo "=== GITHUB SYNC SOBERANO === $DATE"
cd "$DIRIME_PATH" || exit 1
git status --short
git add -A
git commit -m "STACKING UF[H52] :: cristaliza :: suite_soberana_$DATE --[Nudo de Ocho] [term]"
git push origin main
echo "✅ Sync soberano completado"
