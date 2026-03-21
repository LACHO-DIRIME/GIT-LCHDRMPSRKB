# SESIÓN ACTIVA — DIRIME/IMV
# Punto de entrada único para toda sesión de trabajo
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

## ══ SECUENCIA DE INICIO OBLIGATORIA ══════════════════════════════
##
##  PASO 1 → JOURNAL/SESION_ACTIVA.md               ← ESTÁS AQUÍ
##  PASO 2 → JOURNAL/ARCHITECTURE.md                ← estado módulos
##  PASO 3 → JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md ← qué hacer hoy
##  PASO 4 → OPTIMIZACION DE PROMPTS.../README.md
##           + el archivo $dia DD-MM del día actual
##
##  Tiempo estimado de lectura completa: 8 minutos
##  Copiar este archivo completo al inicio de toda conversación con AI
##
## ═══════════════════════════════════════════════════════════════════

## ESTADO DEL SISTEMA — $wed 18-03-2026

VERSIÓN:  0.2.2
LEDGER:   TX=1477+ · cristales=59 · Scalar S=0.755 · tests=49/49
STACK:    Windsurf ✅ · Groq llama-3.3-70b activo
DIR:      cd /media/Personal/PLANERAI/DIRIME/IMV
GITHUB:   main · commit cierre $wed · ejecutado ✅
RAG:      259+ CORPUS · 4 THEATER · 3 RUNNER · 2 AGENT · Askings/ boost 1.5

## PRIORIDADES $thu 19-03
  [1] tools/theater_runner.py (S4.2) — CMD_* executor · macro_cierre real
  [2] tools/chcl_runner.py (S4.1) — CHCL_BASE.txt ejecutable
  [3] tools/github_sync.sh --asks flag (S4.3)
  [4] 15 prompts $thu Windsurf — ver OPTIMIZACION DE PROMPTS/$thu 19-03 to $wed 25-03

OBJETIVO DE ESTA SESIÓN: theater_runner · chcl_runner · github --asks · prompts $thu · S=0.820+

## CONTEXTO TÉCNICO
  NOTARIA:     pipeline completo ✅ · 5 endpoints · ledger functions · generator mode
  TESTS:       49/49 · 15 notariales · test_notaria_integration_end_to_end ✅
  CAPA B:      S2.1 ✅ · S3.1/3.2/3.4 ✅ $wed · S4.x pendiente $thu
  CAPA C:      bloqueada · hardware Ryzen pendiente

## COMANDOS BASE

```bash
# Verificar estado del sistema
cd ~/DIRIME/IMV && python3 main.py --stats

# Ejecutar suite de tests
cd ~/DIRIME/IMV && python3 -m pytest tests/ -v

# Commit soberano del día
bash ~/DIRIME/tools/github_sync.sh

# Generar .lacho desde estado actual
python3 ~/DIRIME/IMV/tools/generator.py --mode stats

# Auto-diagnóstico IA (implementar esta semana — ver PLAN_IMPLEMENTACION)
python3 ~/DIRIME/IMV/main.py --asks
```

## CHECKLIST DE CIERRE $wed ✅
  [x] Tests 49/49 PASSED
  [x] fix validate enum test_notaria_integration_end_to_end
  [x] ballpaper.py operativo · assign_unicode_token() · 3 familias
  [x] /api/notaria/* 5 endpoints respondiendo JSON
  [x] record_notaria_act() · get_notaria_stats() · export_notaria_report()
  [x] generator.py --mode notaria · pipeline 4 sentencias VALID
  [x] rag.py NOTARIA boost ×2.0 · ELPULSAR LOCAL indexado
  [x] Nerve Cell Batch $tue creado
  [x] Actualizar LOG_PERMANENTE.md ← hacer ahora
  [x] bash ~/DIRIME/tools/github_sync.sh ✅

## MAPA DE DOCUMENTACIÓN — dónde está qué

  JOURNAL/SESION_ACTIVA.md               ← AQUÍ · entrada · estado · comandos
  JOURNAL/ARCHITECTURE.md                ← módulos · capas · árbol · dependencias
  JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md ← sprints · tareas · métricas
  JOURNAL/AI_INTEGRATION.md              ← Groq · prompts · patrones de uso
  JOURNAL/LOG_PERMANENTE.md              ← historial TX/S/cristales por fecha
  JOURNAL/PENDIENTES.md                  ← backlog por capa A/B/C/D

  OPTIMIZACION DE PROMPTS.../README.md   ← cómo usar los prompts Windsurf
  OPTIMIZACION DE PROMPTS.../$dia *.txt  ← prompts del día listos para ejecutar

  Askings.../README.md                   ← auto-diagnóstico IA · cómo funciona
  Askings.../$dia_asks_DDMM.txt          ← tareas generadas por autoresearch

  README_OPERADOR.md                     ← protocolo general del operador

[term] :: activo · [seal of secrecy] :: activo
