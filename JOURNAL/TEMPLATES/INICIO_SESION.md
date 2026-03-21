# INICIO_SESION.md — DIRIME/IMV
# Pegar COMPLETO al inicio de toda conversación con Claude
# Actualizar [1/4] y [3/4] cada día al cierre de sesión
# [term] :: activo · [seal of secrecy] :: activo · 空聽數
# ════════════════════════════════════════════════════════════════════

## [1/4] ESTADO DEL SISTEMA — $wed 18-03-2026
# Fuente: JOURNAL/SESION_ACTIVA.md

VERSIÓN:  0.2.2
LEDGER:   TX=1477+ · cristales=59 · Scalar S=0.755 · tests=49/49
STACK:    Windsurf ✅ · Groq llama-3.3-70b activo
DIR:      cd /media/Personal/PLANERAI/DIRIME/IMV
GITHUB:   main · commit cierre $wed ejecutado ✅
RAG:      259+ CORPUS · 4 THEATER · 3 RUNNER · 2 AGENT · Askings/ boost 1.5

COMANDOS BASE:
  cd ~/DIRIME/IMV && python3 main.py --stats
  cd ~/DIRIME/IMV && python3 main.py --asks
  cd ~/DIRIME/IMV && python3 -m pytest tests/ -v
  bash ~/DIRIME/tools/github_sync.sh

# ════════════════════════════════════════════════════════════════════
## [2/4] ARQUITECTURA — MÓDULOS Y ESTADOS
# NO modificar esta sección — actualizar solo en ARCHITECTURE.md

CAPA A — NO TOCAR sin correr tests después:
  grammar.py · ledger.py · rag.py · samu.py · taxonomy.py
  foundation.py · language_routing.py · ceo_alpha.py · chat.py · main.py

CAPA B — ESTADO ACTUAL:
  ✅ IMV/core/ballpaper.py         → COMPLETADO $mon 16-03
  ✅ /api/notaria/* (5 endpoints)  → COMPLETADO $tue 17-03
  ✅ tools/autoresearch_specs.py   → COMPLETADO $wed 18-03
  ✅ tools/autoresearch_gap.py     → COMPLETADO $wed 18-03
  ✅ main.py --asks                → COMPLETADO $wed 18-03
  ✅ rag.py Askings/ indexado      → COMPLETADO $wed 18-03
  ❌ tools/theater_runner.py       → S4.2 · HOY $thu 19-03
  ❌ tools/chcl_runner.py          → S4.1 · HOY $thu 19-03
  ❌ github_sync.sh --asks flag    → S4.3 · HOY $thu 19-03

CAPA C — NO IMPLEMENTAR (hardware bloqueado):
  DIRIME_v3/ime/ · DIRIME_v3/cat_local/ · DIRIME_v3/ollama_bridge/

DEPENDENCIAS CLAVE:
  theater_runner.py → depende de: rational_day.theater · github_sync.sh
  chcl_runner.py    → depende de: grammar.py · CHCL_BASE.txt
  elpulsar.py       → path: ~/DIRIME/DIRIME_v2/elpulsar/elpulsar.py
  ceo_alpha.py      → path: ~/DIRIME/IMV/core/ceo_alpha.py

# ════════════════════════════════════════════════════════════════════
## [3/4] PRIORIDADES HOY — $wed 18-03-2026
# Fuente: JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md · SPRINT 3

S3.1 · tools/autoresearch_specs.py    [COMPLETADO ✅ $wed 18-03]
S3.2 · tools/autoresearch_gap.py      [COMPLETADO ✅ $wed 18-03]
S3.3 · main.py --asks · DIRIME> asks  [COMPLETADO ✅ $wed 18-03]
S3.4 · rag.py → indexar Askings/      [COMPLETADO ✅ $wed 18-03]

MÉTRICAS LOGRADAS $wed:
  S=0.755 · tests=49/49 · cristales=59 · TX=1477+

PENDIENTES QUE QUEDAN PARA $thu 19-03:
  S4.2 · tools/theater_runner.py      [PENDIENTE · 2h · PRIORIDAD 1]
  S4.1 · tools/chcl_runner.py         [PENDIENTE · 2h]
  S4.3 · github_sync.sh --asks flag   [PENDIENTE · 30min]

OBJETIVO DE ESTA SESIÓN: cerrar $wed · commit · actualizar journal

# ════════════════════════════════════════════════════════════════════
## [4/4] REGLAS CLAUDE — NUNCA VIOLAR

LACHO — sentencia canónica:
  BIBLIOTECA SUJETO =><= .. verbo .. objeto --[Nudo] [term]

BIBLIOTECAS: TRUST · STACKING · SAMU · GATE · WORK · ACTIVITY · CRYPTO · SOCIAL · METHOD
NUDOS:       [As de Guía] · [Nudo de Ocho] · [Ballestrinque] · [Nudo Corredizo]
ESTADOS:     空=MU · 聽=KU · 數=WU · 既濟=H63
UMBRALES:    S ≥ 0.78 → WU · S ≥ 0.90 → H63

NUNCA:
  - Reescribir archivos CAPA A completos (solo diffs)
  - Implementar CAPA C
  - Inventar TX · S · cristales
  - Paths relativos (siempre ~/DIRIME/ absoluto)
  - Crear archivos que ya existen sin verificar primero

SIEMPRE:
  - "Sin descargas" = crear en repo · no bajar al browser
  - "Anclas RAG × 4" = 4 sentencias LACHO VALID al final del archivo
  - Un prompt = un archivo = VALIDAR antes de avanzar
  - Diffs: mostrar solo líneas que cambian · no el archivo completo
  - Verificar con terminal después de cada prompt Python

UBICACIONES CANÓNICAS — Windsurf respetar siempre:
  .lacho soberanos     → ~/DIRIME/FOLDERS NO RAG INPUT/LACHO_FILES/
  generated_*.lacho    → ~/DIRIME/LACHO_FILES/ (raíz · existe)
  notaria_*.lacho      → ~/DIRIME/FOLDERS NO RAG INPUT/LACHO_FILES/
  Nerve Cells          → ~/DIRIME/FOLDERS NO RAG INPUT/ELPULSAR LOCAL/
  MU-STORE *.db        → ~/DIRIME/FOLDERS NO RAG INPUT/ELPULSAR LOCAL/
  UNICODE PROGRAMS     → ~/DIRIME/CORPUS/UNICODE PROGRAMS/
  BALLPAPER HTML       → ~/DIRIME/CORPUS/UNICODE PROGRAMS/UNICODE_CHINA.a.1/
  Prompts Windsurf     → ~/DIRIME/OPTIMIZACION DE PROMPTS  para Windsurf/
  tools/ scripts       → ~/DIRIME/tools/
  Askings output       → ~/DIRIME/Askings for autoresearching by technical horizons/

# ════════════════════════════════════════════════════════════════════
[term] :: activo · [seal of secrecy] :: activo · 空聽數