# Askings for autoresearching by technical horizons
# DIRIME/IMV · Motor de auto-diagnóstico soberano
#
# Este directorio NO es parte de la secuencia de inicio.
# Es el motor que genera los inputs para la secuencia.
# Leer cuando: implementando autoresearch · ejecutando --asks
#
# ALIMENTA → OPTIMIZACION DE PROMPTS.../README.md (PASO 4)
#
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

## QUÉ ES ESTE DIRECTORIO

Auto-diagnóstico ejecutable del ecosistema DIRIME.
El sistema observa su propio estado → detecta gaps técnicos →
genera tareas LACHO accionables priorizadas por Groq.

No es un log manual. No es documentación estática.
Es el punto donde el sistema se pregunta a sí mismo qué hacer hoy.

## CÓMO FUNCIONA (flujo completo)
```
[Python local]                    [Groq llama-3.3-70b]
autoresearch_specs.py             autoresearch_gap.py
  escanea filesystem         →      context_package → bridge.translate()
  sovereign.db vía PEEK            system_prompt soberano
  clasifica: ACTIVE/DECLARED/      priorización por Scalar S
  STUB/BLOCKED                     output: sentencias LACHO
       ↓                                      ↓
actual_structure.json         $dia_asks_DDMM.txt
sorted_upgrading.yml          JOURNAL/PENDIENTES.md (append)
                              sovereign.db (POKE fabric_state)
```

## EJECUTAR
```bash
# Desde IMV/:
python3 main.py --asks

# Desde modo interactivo:
DIRIME> asks

# Directo:
python3 ~/DIRIME/tools/autoresearch_gap.py
```

## ARCHIVOS DEL DIRECTORIO
```
README.md                  ← este archivo · contexto y entorno
autoresearch_specs.py      ← scanner repo → JSON+YAML (sin Groq)
autoresearch_gap.py        ← detector gaps + Groq → $dia_asks
actual_structure.json      ← AUTO-GENERADO por specs.py
sorted_upgrading.yml       ← AUTO-GENERADO · módulos rankeados
$dia_asks_DDMM.txt         ← AUTO-GENERADO · tareas del día
```

## FORMATO DE UN $dia_asks (qué produce)
```
// ASKING · $sat 14-03 · autoresearch soberano · Groq llama-3.3-70b
// TX=1335 · cristales=42 · S=0.78 · gaps=N detectados
// horizonte activo: CAPA_B · hardware antiX · Groq API

ASK_01 | ALTA | CAPA_B | ~2h
  WORK {actuator} =><= .. implementa .. core_ballpaper_tabla_3_familias --[As de Guía] [term]
  impacto: desbloquea assign_unicode_token() + 3 tests pendientes
  desbloquea: ledger.py → generator.py → chat.py ballpaper_render()

ASK_02 | ALTA | CAPA_B | ~1h
  WORK {actuator} =><= .. agrega .. notaria_endpoints_main_py --[Nudo de Ocho] [term]
  impacto: 4 UNICODE PROGRAMS apuntan a estos endpoints sin receptor
  desbloquea: KALIL pipeline completo · notaria.runner ejecutable

ASK_03 | MEDIA | CAPA_B | ~3h
  WORK {actuator} =><= .. crea .. tools_chcl_runner_ejecutor_minimo --[As de Guía] [term]
  impacto: CHCL_BASE.txt PROCEDURE DIVISION sin ejecutor Python
  desbloquea: CHCL portabilidad · CEO de LACHO operativo

// BLOQUEADOS — no implementar hasta hardware disponible:
ASK_BLOCKED_01: DIRIME_v3/ime/ → requiere Ollama + PC Ryzen
ASK_BLOCKED_02: DIRIME_v3/cat_local/ → requiere segundo nodo físico
ASK_BLOCKED_03: DIRIME_v3/ollama_bridge/ → swap Groq→Ollama · PC Ryzen

[term] :: activo · generado por autoresearch_gap.py + Groq
```

## SEÑALES UNICODE QUE EL DETECTOR LEE

El scanner reconoce estas señales en archivos del corpus para
identificar gaps entre lo declarado y lo implementado:
```
[trust. term= ...]     → nuevo term declarado → verificar Python
[term=: ..]            → asignación soberana → verificar sovereign.db
{masking=: ..}         → masking → verificar grammar.py
Term.ejemplo=..        → ejemplo declarativo → verificar test_imv.py
equation.ejemplo=..    → METHOD <equation> → verificar IMV/core/
UNICODE: TOKEN_X       → token declarado → verificar función Python
RAG_ANCHOR: FILE.txt   → ancla → verificar que el archivo existe
```

Lenguajes escaneados: `.lacho` · `.py` · `.txt` · `.theater`
· `.runner` · `.blue` · `.green` · `.gate`

## ESTADOS DE IMPLEMENTACIÓN (sorted_upgrading.yml)
```yaml
# 4 estados soberanos · generado por autoresearch_specs.py
ACTIVE:    implementado + tests + ancla RAG existente
DECLARED:  en CORPUS pero sin Python correspondiente
STUB:      .gitkeep o archivo < 50 bytes · diseño pendiente
BLOCKED:   requiere hardware/infraestructura no disponible hoy
```

## PREGUNTAS QUE ESTE SISTEMA RESPONDE

Python puro (sovereign.db):
  - ¿Cuál es el Scalar S actual y qué lo está bajando?
  - ¿Cuántos tokens UNICODE están declarados sin implementación?
  - ¿Qué verbos están cerca del umbral de cristalización?
  - ¿Qué anclas RAG referencian archivos que no existen?
  - ¿Cuántos tests pasarían si se implementa módulo X?

Groq (razonamiento sobre contexto):
  - ¿Qué implementar primero para llegar a S=0.840?
  - ¿Qué módulo declarado desbloquea más otros?
  - ¿Hay inconsistencias entre PENDIENTES.md y sovereign.db?
  - ¿Cuándo conviene mover un asking de CAPA_C a CAPA_B?

## HORIZONTE TÉCNICO: CAPAS

| Capa  | Estado      | Condición                        | Asks generados  |
|-------|-------------|----------------------------------|-----------------|
| A     | COMPLETO ✅  | grammar+ledger+rag+samu operativos| ninguno         |
| B     | ACTIVO ⚡    | hardware actual · antiX · Groq   | ASK_01..N       |
| C     | BLOQUEADO 🔒 | PC Ryzen + Ollama local           | ASK_BLOCKED_*   |
| D     | FUTURO 🌐   | 2 nodos físicos + HL FABRIC real  | ASK_FUTURE_*    |

Los asks CAPA_C y D se acumulan como bloqueados hasta que
el hardware esté disponible. No se implementan antes.

## INTEGRACIÓN CON EL REPO
```
Askings/ lee desde:
  sovereign.db          ← poke_peek.py PEEK
  JOURNAL/PENDIENTES.md ← gaps manuales previos
  IMV/core/*.py         ← módulos implementados
  CORPUS/UNICODE PROGRAMS/*.txt ← tokens declarados
  CORPUS/BIBLIA/*.txt   ← anclas RAG existentes

Askings/ escribe hacia:
  $dia_asks_DDMM.txt    ← tareas del día
  JOURNAL/PENDIENTES.md ← append automático
  sovereign.db          ← POKE fabric_state
  git (via github_sync.sh) ← commit de asks
```

## ESTADO HOY $sat 14-03
```
autoresearch_specs.py  → PENDIENTE · P3 en plan de implementación
autoresearch_gap.py    → PENDIENTE · P4 en plan
actual_structure.json  → no existe · se genera al ejecutar specs.py
sorted_upgrading.yml   → no existe · se genera al ejecutar specs.py

Gaps conocidos hoy (hasta que P4 exista, manual):
  GAP_01: IMV/core/ballpaper.py → declarado, sin implementar
  GAP_02: /api/notaria/* endpoints → sin receptor en main.py
  GAP_03: tools/chcl_runner.py → referenciado, sin crear
  GAP_04: tools/theater_runner.py → referenciado, sin crear
  GAP_05: DIRIME_v3/ → esqueleto vacío, bloqueado hardware
```

[term] :: activo · [seal of secrecy] :: activo · 空聽數

