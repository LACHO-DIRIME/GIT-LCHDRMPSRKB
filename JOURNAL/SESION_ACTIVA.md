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

## ESTADO DEL SISTEMA — $sun 15-03-2026

VERSIÓN:  0.2.1
LEDGER:   TX=1363 · cristales=46 · Scalar S=0.773 · tests=44/44
STACK:    Windsurf ✅ · Groq llama-3.3-70b activo
DIR:      cd /media/Personal/PLANERAI/DIRIME/IMV
GITHUB:   main · commit cierre $sun completado
RAG:      252 CORPUS · 4 THEATER · 3 RUNNER · 2 AGENT · 14 patrones
SAMU:     IDLE · 0 disputas · lacho_score=0.8

## PRÓXIMOS CRISTALES
  certifica × 10 → ✨ CRISTAL
  detiene   × 10 → ✨ CRISTAL

## PRIORIDADES $mon 16-03
  [1] /api/notaria/* — 5 endpoints en main.py (S2.1 · prereq: ballpaper.py)
  [2] tools/autoresearch_specs.py — scanner repo sin Groq (S2.2)
  [3] Askings/$sat_asks_14-03.txt — ejemplo manual formato asks (S2.3)
  [4] IMV/core/ballpaper.py — tabla 3 familias (S1.2 · aún pendiente)

## CONTEXTO TÉCNICO
  NOTARIA:     grammar H63+sella · taxonomy N0-N4 · pipeline 44/44
  LACHO_FILES: 10 generated ingresados · 105/135 VALID
  CAPA B:      activa · implementación en curso
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

## CHECKLIST DE CIERRE
  [ ] Actualizar ESTADO DEL SISTEMA arriba (TX · S · tests · fecha)
  [ ] Agregar línea a JOURNAL/LOG_PERMANENTE.md
  [ ] Marcar tareas completadas en PLAN_IMPLEMENTACION_BLOQUE_B.md
  [ ] bash ~/DIRIME/tools/github_sync.sh

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
