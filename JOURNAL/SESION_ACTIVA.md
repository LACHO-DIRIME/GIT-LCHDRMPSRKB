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

## ESTADO DEL SISTEMA — $mon 16-03-2026

VERSIÓN:  0.2.1
LEDGER:   TX=1387 · cristales=49 · Scalar S=0.768 · tests=44/44
STACK:    Windsurf ✅ · Groq llama-3.3-70b activo
DIR:      cd /media/Personal/PLANERAI/DIRIME/IMV
GITHUB:   main · commit cierre $mon pendiente
RAG:      258 CORPUS · 4 THEATER · 3 RUNNER · 2 AGENT

## PRIORIDADES $tue 17-03
  [1] ballpaper.py — COMPLETADO ✅ commit c80097d
  [2] /api/notaria/* endpoints — verificar con ballpaper integrado
  [3] tools/autoresearch_specs.py (S2.2)

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
  [x] Actualizar ESTADO DEL SISTEMA arriba (TX · S · tests · fecha)
  [x] Agregar línea a JOURNAL/LOG_PERMANENTE.md
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
