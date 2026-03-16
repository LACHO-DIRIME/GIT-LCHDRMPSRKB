# PLAN IMPLEMENTACIÓN — CAPA_B COMPLETO
# DIRIME/IMV · $sat 14-03-2026 → objetivo S=0.840
#
# SECUENCIA: [PASO 3 de 4]
#   ← PASO 2: JOURNAL/ARCHITECTURE.md
#   → PASO 4: OPTIMIZACION DE PROMPTS.../README.md + $dia *.txt
#
# [term] :: activo

## ESTADO BASE
TX=1335 · cristales=42 · S=0.78 · tests=44/44 · VERSION=0.2.1

## SPRINT 1 — HOY $sat 14-03 (esta sesión)

### S1.1 · Commit final $fri (prerequisito de todo)
```bash
cd ~/DIRIME
# Comando completo en SESION_ACTIVA.md → ejecutar primero
git add ... && git commit -m "..." && git push origin main
```
Estado: PENDIENTE · Tiempo: 5 min · Bloquea: todo lo demás

### S1.2 · IMV/core/ballpaper.py
Implementar tabla 3 familias + assign_unicode_token()
Impacto: +2-3 tests · desbloquea ledger+generator+chat
Tiempo: ~2h · Prerequisito: S1.1
COMPLETADO: $mon 16-03 · 3 familias (ACCION/REGISTRO/AUDITORIA) · assign_unicode_token() · ballpaper_render() · ballpaper_render_notaria() · tests 44/44 verdes

### S1.3 · ledger.py → usar assign_unicode_token()
Llamar ballpaper.assign_unicode_token() al cristalizar verbo
Tiempo: ~30 min · Prerequisito: S1.2

### S1.4 · Askings/README.md reemplazar
Usar el README de DOCUMENTO 1 de este archivo
Tiempo: 5 min · sin prerequisitos

## SPRINT 2 — $mon-$tue 16-17/03

### S2.1 · /api/notaria/* en main.py (5 endpoints) ✅
certifica · sella · inmutabiliza · verifica · export
Impacto: desbloquea KALIL pipeline completo
Tiempo: ~3h · Prerequisito: ballpaper.py
COMPLETADO: main.py --notaria cmd implementado · language_routing extendido · test integración

### S2.2 · tools/autoresearch_specs.py ✅
Scanner filesystem + sovereign.db → JSON + YAML
Sin Groq · Python stdlib puro
Tiempo: ~2h · sin prerequisitos adicionales
COMPLETADO: Especificaciones creadas · estructura definida

### S2.3 · Askings/$sat_asks_14-03.txt manual ✅
Crear ejemplo manual del formato de asks
Usar los gaps conocidos documentados en ARCHITECTURE.md
Tiempo: 30 min

## SPRINT 3 — $wed-$thu 18-19/03

### S3.1 · tools/autoresearch_gap.py
Gap detector + Groq bridge → $dia_asks_DDMM.txt
Prerequisito: autoresearch_specs.py + bridge.py activo
Tiempo: ~3h

### S3.2 · main.py --asks · DIRIME> asks
Integrar autoresearch como comando del sistema
Tiempo: ~1h · Prerequisito: S3.1

### S3.3 · JOURNAL/ARCHITECTURE.md crear
Usar el contenido de DOCUMENTO 2 de este plan
Tiempo: 10 min

### S3.4 · rag.py → indexar Askings/
Agregar _ASKINGS_DIR a _SOVEREIGN_SOURCES con boost 1.5
Tiempo: 15 min

## SPRINT 4 — $fri-$sat 20-21/03

### S4.1 · tools/chcl_runner.py
Ejecutor mínimo CHCL → lee CHCL_BASE.txt → ejecuta LACHO
Tiempo: ~2h

### S4.2 · tools/theater_runner.py
Ejecutor CMD_* de .theater → descomenta macro_cierre
Tiempo: ~2h

### S4.3 · tools/github_sync.sh --asks flag
Agregar stage para $dia_asks_DDMM.txt en commit
Tiempo: 30 min

## SPRINT 5 — semana 19-25/03 (según PLAN MENSUAL)

### S5.1 · UNICODE METHOD × 4 NEURONAS
Según OPTIMIZACION DE PROMPTS $thu 19-03 to $wed 25-03
12 tareas detalladas en ese archivo

## MÉTRICAS OBJETIVO

| Sprint | Tests | Cristales | Scalar S | Módulos nuevos |
|--------|-------|-----------|----------|----------------|
| S1     | 44+   | 42+       | 0.790    | ballpaper      |
| S2     | 46+   | 43+       | 0.800    | notaria API    |
| S3     | 48+   | 44+       | 0.820    | autoresearch   |
| S4     | 50+   | 45+       | 0.835    | chcl+theater   |
| S5     | 52+   | 46+       | 0.840    | METHOD×neuronas|

## CRITERIO DE ÉXITO CAPA_B COMPLETO
  S=0.840+ · tests=50+ · cristales=45+
  autoresearch operativo · ciclo diario automatizable
  notaria pipeline completo · CHCL ejecutable

[term] :: activo · [seal of secrecy] :: activo · 空聽數