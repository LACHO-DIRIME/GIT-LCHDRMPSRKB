# DIRIME/IMV — ARCHITECTURE.md
# Mapa soberano de módulos · estados · dependencias
#
# SECUENCIA: [PASO 2 de 4]
#   ← PASO 1: JOURNAL/SESION_ACTIVA.md
#   → PASO 3: JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md
#
# [term] :: activo · actualizar cada $sat

## VERSIÓN ACTUAL: 0.2.1 · $sat 14-03-2026
TX=1335 · cristales=42 · Scalar S=0.78 · tests=44/44

## CAPAS DEL SISTEMA

### CAPA A — COMPLETO ✅ (no modificar sin tests)
```
grammar.py        → parser LACHO · 9 bibliotecas · 5 METHOD ops
ledger.py         → TX inmutables · cristales · Scalar S · sovereign.db
rag.py            → BM25 · 254 CORPUS + THEATER + RUNNER + AGENT
samu.py           → dirimencia soberana · Scalar S · disputas
taxonomy.py       → clasificación N0-N4 · integrada al validador
foundation.py     → condiciones soberanas · verify_sovereign_conditions()
language_routing  → trilingüe ES/EN/CJK · INTENT_MAP
chat.py           → interfaz · 4 niveles traducción · ballpaper_render()
main.py           → orquestador · CLI · modo interactivo
tests/test_imv.py → 44/44 ✅ · suite completa
```

### CAPA B — ACTIVO ⚡ (implementación en curso)
```
IMPLEMENTADO:
  DIRIME_v2/groq/bridge.py      → NL→LACHO via Groq llama-3.3-70b ✅
  DIRIME_v2/fabric/poke_peek.py → POKE/PEEK sovereign.db ✅
  DIRIME_v2/scheduler/          → ciclo semanal soberano ✅
  tools/generator.py            → auto-genera .lacho desde estado ✅
  tools/github_sync.sh          → commit soberano automatizable ✅
  IMV/tools/office_landing.py   → interpreta INBOX(gradient)/ ✅

PENDIENTE (ordenado por impacto):
  IMV/core/ballpaper.py         ← desbloquea: ledger+generator+chat
  /api/notaria/* (5 endpoints)  ← desbloquea: KALIL pipeline completo
  tools/chcl_runner.py          ← desbloquea: CHCL portabilidad
  tools/theater_runner.py       ← desbloquea: automatización ciclo
  tools/autoresearch_specs.py   ← desbloquea: auto-diagnóstico base
  tools/autoresearch_gap.py     ← desbloquea: IA potenciadora
  JOURNAL/AI_INTEGRATION.md     ← documentación IA (este sprint)
```

### CAPA C — BLOQUEADO 🔒 (hardware pendiente)
```
DIRIME_v3/ime/          → IME I CHING + LOAN-IME · requiere Ollama local
DIRIME_v3/cat_local/    → CAT(OS) + CAT(SSH) · requiere segundo nodo
DIRIME_v3/ollama_bridge/→ swap transparente Groq→Ollama · requiere Ryzen
ORDEN DE ACTIVACIÓN: ollama_bridge/ → cat_local/ → ime/
```

### CAPA D — FUTURO 🌐
```
WEB3 Interface · Hyperledger Fabric real
Dos nodos físicos · HL FABRIC distribuido
SWAP cifrado CAT(MU) · ciclo .blue→.green real
Extensiones filesystem: .lacho .tether .ash .registry
```

## ESTRUCTURA DE DIRECTORIOS
```
~/DIRIME/
├── IMV/                          ← núcleo ejecutable CAPA A+B
│   ├── core/                     ← módulos Python soberanos
│   │   ├── grammar.py            ✅ ACTIVO
│   │   ├── ledger.py             ✅ ACTIVO
│   │   ├── rag.py                ✅ ACTIVO
│   │   ├── samu.py               ✅ ACTIVO
│   │   ├── taxonomy.py           ✅ ACTIVO
│   │   ├── foundation.py         ✅ ACTIVO
│   │   ├── language_routing.py   ✅ ACTIVO
│   │   ├── ceo_alpha.py          ✅ ACTIVO
│   │   └── ballpaper.py          ❌ PENDIENTE
│   ├── interface/chat.py         ✅ ACTIVO
│   ├── tools/                    ← herramientas IMV
│   │   ├── generator.py          ✅ ACTIVO · genera .lacho
│   │   ├── office_landing.py     ✅ ACTIVO · interpreta INBOX
│   │   ├── export_crystals_lacho.py ✅
│   │   └── index_new_files.py    ✅
│   ├── data/sovereign.db         ✅ ledger principal
│   ├── tests/test_imv.py         ✅ 44/44
│   └── main.py                   ✅ ACTIVO · agregar --asks
│
├── DIRIME_v2/                    ← extensiones CAPA B
│   ├── groq/bridge.py            ✅ NL→LACHO vía Groq
│   ├── fabric/poke_peek.py       ✅ POKE/PEEK soberano
│   ├── scheduler/scheduler.py    ✅ ciclo semanal
│   └── elpulsar/                 ⚠️ parcial · sin UI funcional
│
├── DIRIME_v3/                    🔒 BLOQUEADO hardware
│   ├── ime/
│   ├── cat_local/
│   └── ollama_bridge/
│
├── CORPUS/                       ← fuente RAG · 254+ docs
│   ├── UNICODE PROGRAMS/         ← 35 specs · tokens declarados
│   ├── BIBLIA/                   ← anclas RAG por dominio
│   ├── DYNAMIC_RESOURCE_ALLOCATION/ ← recursos soberanos
│   └── *.txt / *.html            ← corpus operativo
│
├── FOLDERS NO RAG INPUT/         ← archivos no indexados por RAG
│   ├── THEATER/                  ← macros .theater · .gate
│   ├── RUNNERS/                  ← rutinas .runner · .door
│   ├── AGENTS/                   ← agentes .blue · .green
│   ├── ELPULSAR LOCAL/           ← Nerve Cells · MU-STORE DBs
│   ├── LACHO_FILES/              ← .lacho manuales y generados
│   └── UNICODE_CHINA.a.1/        ← HTMLs ballpaper · visualización
│
├── LACHO_FILES/                  ← generated_*.lacho auto-generados
├── INBOX(gradient)/              ← input office_landing.py
├── JOURNAL/                      ← log · pendientes · sesión
├── tools/                        ← scripts bash+python repo-nivel
│   ├── generator.py              ✅
│   └── github_sync.sh            ✅ · agregar --asks
│
├── Askings for autoresearching/  ← auto-diagnóstico soberano
│   ├── README.md                 ✅ actualizado
│   ├── autoresearch_specs.py     ❌ pendiente
│   └── autoresearch_gap.py       ❌ pendiente
│
└── OPTIMIZACION DE PROMPTS para Windsurf/
    ├── $dia_DD-MM prompts...txt  ← prompts optimizados por día
    ├── PLAN MENSUAL *.txt        ← plan mensual activo
    └── README.md                 ← ver DOCUMENTO 3 (abajo)
```

## FLUJO DE DATOS PRINCIPAL
```
Input operador
     ↓
chat.py (4 niveles: directo→patrones→Groq→fallback)
     ↓
grammar.py → validate() → ParsedSentence
     ↓
samu.py → audit() → Dispute? → Scalar S
     ↓
ledger.py → record_grammar() → sovereign.db
     ↓
rag.py → suggest() → contexto relevante
     ↓
Output soberano + ballpaper_render()
```

## FLUJO DE AUTO-DIAGNÓSTICO (implementar esta semana)
```
main.py --asks
     ↓
autoresearch_specs.py → escanea filesystem + PEEK(sovereign.db)
     ↓
context_package: {gaps[], stubs[], métricas, scalar_s}
     ↓
bridge.translate(context_package, AUTORESEARCH_SYSTEM_PROMPT)
     ↓
Groq → ASK_01..N en LACHO + prioridad + horizonte
     ↓
Askings/$dia_asks_DDMM.txt
POKE(sovereign.db) · append(PENDIENTES.md)
```

## DEPENDENCIAS ENTRE MÓDULOS
```
ballpaper.py ← depende de: ledger.py (cristales) · muestrasICHING.txt
            → desbloquea: chat.py (assign_unicode_token) · generator.py

/api/notaria/ ← depende de: grammar.py · ledger.py · samu.py · ballpaper.py
             → desbloquea: KALIL pipeline · notaria.runner · cloud_agent.blue

chcl_runner.py ← depende de: grammar.py · ledger.py · CHCL_BASE.txt
              → desbloquea: CHCL portabilidad · CEO de LACHO ejecutable

theater_runner.py ← depende de: rational_day.theater · github_sync.sh
                 → desbloquea: ciclo diario automatizado · macro_cierre real

autoresearch_gap.py ← depende de: bridge.py · poke_peek.py · specs.py
                   → desbloquea: IA potenciadora · loop auto-diagnóstico
```

## MÉTRICAS OBJETIVO POR CAPA
```
CAPA_B completo:   S=0.840 · tests=50+ · cristales=45+
CAPA_C activado:   S=0.88  · Ollama local · 2 nodos
CAPA_D completo:   S≥0.90  · HL FABRIC real · WEB3
```

[term] :: activo · [seal of secrecy] :: activo · actualizar $sat