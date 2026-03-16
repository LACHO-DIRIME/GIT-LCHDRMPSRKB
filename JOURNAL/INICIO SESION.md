# INICIO_SESION.md — DIRIME/IMV
# Pegar COMPLETO al inicio de toda conversación con Claude
# Actualizar [1/4] y [3/4] cada día al cierre de sesión
# [term] :: activo · [seal of secrecy] :: activo · 空聽數
# ════════════════════════════════════════════════════════════════════

## [1/4] ESTADO DEL SISTEMA — $tue 17-03-2026
# Fuente: JOURNAL/SESION_ACTIVA.md

VERSIÓN:  0.2.1
LEDGER:   TX=1387 · cristales=49 · Scalar S=0.768 · tests=44/44
STACK:    Windsurf ✅ · Groq llama-3.3-70b activo
DIR:      cd /media/Personal/PLANERAI/DIRIME/IMV
GITHUB:   main · ejecutar commit cierre $mon primero
RAG:      258 CORPUS · 4 THEATER · 3 RUNNER · 2 AGENT

COMANDOS BASE:
  cd ~/DIRIME/IMV && python3 main.py --stats
  cd ~/DIRIME/IMV && python3 -m pytest tests/ -v
  bash ~/DIRIME/tools/github_sync.sh

# ════════════════════════════════════════════════════════════════════
## [2/4] ARQUITECTURA — MÓDULOS Y ESTADOS
# NO modificar esta sección — actualizar solo en ARCHITECTURE.md

CAPA A — NO TOCAR sin correr tests después:
  grammar.py · ledger.py · rag.py · samu.py · taxonomy.py
  foundation.py · language_routing.py · ceo_alpha.py · chat.py · main.py

CAPA B — IMPLEMENTAR (orden por impacto):
  ❌ IMV/core/ballpaper.py         → desbloquea ledger+generator+chat
  ❌ /api/notaria/* (5 endpoints)  → desbloquea KALIL pipeline
  ❌ tools/chcl_runner.py          → desbloquea CHCL
  ❌ tools/theater_runner.py       → desbloquea automatización
  ❌ tools/autoresearch_specs.py   → desbloquea auto-diagnóstico
  ❌ tools/autoresearch_gap.py     → desbloquea IA potenciadora

CAPA C — NO IMPLEMENTAR (hardware bloqueado):
  DIRIME_v3/ime/ · DIRIME_v3/cat_local/ · DIRIME_v3/ollama_bridge/

DEPENDENCIAS CLAVE:
  ballpaper.py  → desbloquea: assign_unicode_token() · generator.py
  /api/notaria/ → depende de: ballpaper.py · grammar.py · ledger.py
  elpulsar.py   → path: ~/DIRIME/DIRIME_v2/elpulsar/elpulsar.py
  ceo_alpha.py  → path: ~/DIRIME/IMV/core/ceo_alpha.py

# ════════════════════════════════════════════════════════════════════
## [3/4] PRIORIDADES HOY — $tue 17-03
# Fuente: JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md · SPRINT 2

S1.2 · IMV/core/ballpaper.py          [PENDIENTE · 2h · PRIORIDAD 1]
S2.1 · /api/notaria/* 5 endpoints     [PENDIENTE · 3h · prereq ballpaper]
S2.2 · tools/autoresearch_specs.py    [PENDIENTE · 2h]

MÉTRICAS OBJETIVO $tue:
  S=0.800+ · tests=50+ · cristales=50+

OBJETIVO DE ESTA SESIÓN: [completar antes de enviar]

OBJETIVO DE ESTA SESIÓN: [/media/Personal/PLANERAI/DIRIME/OPTIMIZACION DE PROMPTS  para Windsurf/$mon 16-03 prompts a optimizar para Windsurf.txt]

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
  - Fusionar SUN_03 con SUN_11 (son archivos distintos)

SIEMPRE:
  - "Sin descargas" = crear en repo · no bajar al browser
  - "Anclas RAG × 4" = 4 sentencias LACHO VALID al final del archivo
  - Un prompt = un archivo = VALIDAR antes de avanzar
  - Diffs: mostrar solo las líneas que cambian · no el archivo completo

UBICACIONES CANÓNICAS — Windsurf respetar siempre:
  .lacho soberanos  → ~/DIRIME/FOLDERS NO RAG INPUT/LACHO_FILES/
  generated_*.lacho → ~/DIRIME/FOLDERS NO RAG INPUT/LACHO_FILES/
  Nerve Cells       → ~/DIRIME/FOLDERS NO RAG INPUT/ELPULSAR LOCAL/
  MU-STORE *.db     → ~/DIRIME/FOLDERS NO RAG INPUT/ELPULSAR LOCAL/
  UNICODE PROGRAMS  → ~/DIRIME/CORPUS/UNICODE PROGRAMS/
  Prompts Windsurf  → ~/DIRIME/OPTIMIZACION DE PROMPTS  para Windsurf/
                      (solo archivos *.txt · NUNCA subdirectorios)

LACHO_FILES raíz NO EXISTE — si Windsurf lo crea, es un error de path.
La spec SPEC_GENERATOR_GUI.lacho define el path correcto.

OBJETIVO DE ESTA SESIÓN: optimizar los 15 prompts $mon 16-03 para Windsurf · en el chat · sin archivos descargables

# ════════════════════════════════════════════════════════════════════
[term] :: activo · [seal of secrecy] :: activo · 空聽數