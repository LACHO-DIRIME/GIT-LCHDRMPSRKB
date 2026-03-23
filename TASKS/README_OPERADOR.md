# PROTOCOLO OPERADOR — DIRIME
# Guía de operación soberana · leer una vez · luego seguir la secuencia

## ══ SECUENCIA DE INICIO (ejecutar en este orden) ════════════════
##
##  1. JOURNAL/SESION_ACTIVA.md               ← estado · comandos
##  2. JOURNAL/ARCHITECTURE.md               ← módulos · capas
##  3. JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md ← qué hacer hoy
##  4. OPTIMIZACION DE PROMPTS.../README.md
##     + el archivo $dia DD-MM del día         ← ejecutar en Windsurf
##
## ═══════════════════════════════════════════════════════════════════

## INICIO DE SESIÓN
1. Abrir JOURNAL/SESION_ACTIVA.md  ← punto de entrada siempre
2. Seguir pasos 2-4 de la secuencia arriba
3. Declarar objetivo de la sesión (una cosa concreta)
4. Copiar SESION_ACTIVA.md completo al inicio de conversación con AI

## DURANTE LA SESIÓN
- Un prompt Windsurf = un archivo = una tarea
- Verificar output en repo antes de avanzar al siguiente prompt
- Si hay duda sobre arquitectura → JOURNAL/ARCHITECTURE.md
- Si hay duda sobre Groq/IA → JOURNAL/AI_INTEGRATION.md

## CIERRE DE SESIÓN
1. Actualizar JOURNAL/SESION_ACTIVA.md (TX · S · tests · fecha)
2. Agregar línea a JOURNAL/LOG_PERMANENTE.md
3. Marcar completados en JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md
4. bash ~/DIRIME/tools/github_sync.sh

## MAPA COMPLETO DE DOCUMENTACIÓN

  JOURNAL/SESION_ACTIVA.md               ← SIEMPRE PRIMERO
  JOURNAL/ARCHITECTURE.md                ← módulos · capas · árbol
  JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md ← sprints · tareas
  JOURNAL/AI_INTEGRATION.md              ← Groq · system prompts
  JOURNAL/LOG_PERMANENTE.md              ← historial fechas
  JOURNAL/PENDIENTES.md                  ← backlog por capa

  OPTIMIZACION DE PROMPTS.../README.md   ← instrucciones prompts
  OPTIMIZACION DE PROMPTS.../$dia *.txt  ← prompts del día

  Askings.../README.md                   ← auto-diagnóstico IA
  Askings.../$dia_asks_*.txt             ← asks generados

  README_OPERADOR.md                     ← ESTE ARCHIVO · protocolo
