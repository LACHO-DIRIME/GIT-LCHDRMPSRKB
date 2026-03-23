# LEARNING/LEARNING_CYCLE.md
# El ciclo soberano de absorción: READ → REFLECT → RELATE → REAP
# Protocolo operativo completo · integrado con IMV
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

====================================================================
## POSICIÓN EN LEARNING/

```
README.md           → 14 focos · definiciones · mapa completo
LEARNING_CYCLE.md   → ciclo R4 operativo ← ESTE
THREATS.md          → POLLUTE · MANIPULATE · NO VALUES · protocolos
TEMPORAL.md         → ANTRO/PRO/RETROGRADE · PROSPECTIVE/RETROSPECTIVE
WEEKLY_RITUAL.md    → protocolo semanal canónico
```

====================================================================
## EL CICLO R4 — VISIÓN COMPLETA

```
              STRATEGIC ABSORPTION (intención declarada)
                           │
                    RELIABLE (fuente ok)
                           │
              ─────────────▼─────────────
              │                         │
         [input externo]         [histórico IMV]
              │                         │
              ▼                         ▼
           READ                   RETROSPECTIVE
         (空 MU)                  (Behavioral RAG)
              │                         │
              └──────────┬──────────────┘
                         ▼
                      REFLECT
                     (聽 KU)
                      SAMU @
                         │
                      RELATE
                    (KU activo)
                    RAG search
                         │
                ┌────────┴────────┐
                ▼                 ▼
        [conecta bien]    [no conecta / falla]
                │                 │
              REAP           RETROGRADE
            (數 WU)          (corregir)
           cristaliza
```

====================================================================
## FASE 1 — READ · 空 MU · DURACIÓN RECOMENDADA: 20-40 min

### Qué es
El primer contacto con el material. El operador está en MU —
espacio vacío antes de cualquier juicio. No hay sentencias, no
hay commits, no hay cristales todavía.

### Comandos IMV en fase READ
```bash
# Verificar que el sistema está en estado limpio antes de absorber
cd ~/DIRIME/IMV && python3 main.py --stats
# → registrar TX/S/cristales ANTES de iniciar · baseline de la sesión

# NO ejecutar validaciones todavía
# NO abrir grammar.py todavía
# NO modificar nada del corpus todavía
```

### Checklist READ
```
[ ] Leer el material completo sin interrupciones
[ ] No tomar notas de implementación todavía
[ ] Registrar: ¿qué pregunta responde este material?
[ ] Registrar: ¿qué contradicción evidente introduce?
[ ] Verificar fuente: ¿pasa el filtro RELIABLE?
[ ] Tiempo: 20-40 min según densidad del material
```

### Señal de READ completo
El operador puede resumir el material en 3 sentencias canónicas
LACHO sin haber ejecutado ninguna línea de código.

### Señal de READ fallido
El operador empieza a modificar archivos durante la lectura →
parar → volver a MU → terminar READ primero.

```
LACHO: GATE UF[H05] =><= .. espera .. read_completo_sin_emision --[Nudo Corredizo] [term]
```

====================================================================
## FASE 2 — REFLECT · 聽 KU · DURACIÓN RECOMENDADA: 15-30 min

### Qué es
Procesamiento interno del material leído. SAMU @ está activo —
auditoría interna antes de conectar con el corpus. El operador
escucha activamente las tensiones que el material genera.

### Las 5 preguntas REFLECT
```
1. ¿Qué biblioteca LACHO principal activa este material?   (TRUST / GATE / SAMU / CRYPTO / STACKING / SOCIAL / METHOD / ACTIVITY / WORK)

2. ¿Qué cristal existente refuerza o contradice?
   python3 main.py --cristales | grep [término_relevante]

3. ¿Qué test existente podría fallar si aplico esto?
   grep -r "[término]" ~/DIRIME/IMV/tests/test_imv.py

4. ¿Qué está en PENDIENTES.md que esto resuelve?
   grep -i "[término]" ~/DIRIME/JOURNAL/PENDIENTES.md

5. ¿Cuál es el Scalar S mínimo requerido para implementar esto?
   (ver TAXONOMY_MAP en grammar.py: cada biblioteca tiene scalar_min)
```

### Comandos IMV en fase REFLECT
```bash
# Verificar cristales actuales · ¿alguno relacionado?
cd ~/DIRIME/IMV && python3 main.py --cristales

# Verificar distribución por biblioteca · ¿dónde está el gap?
python3 main.py --bibliotecas

# Verificar pendientes · ¿esto responde algún ASK?
cat ~/DIRIME/JOURNAL/PENDIENTES.md | grep -A3 "CAPA B"
cat ~/DIRIME/Askings\ for\ autoresearching\ by\ technical\ horizons/*.txt 2>/dev/null | head -30
```

### Señal de REFLECT completo
El operador puede responder las 5 preguntas con respuestas
verificables (no especulativas).

```
LACHO: SAMU @ =><= .. audita .. reflect_5_preguntas_respondidas --[Ballestrinque] [term]
```

====================================================================
## FASE 3 — RELATE · KU ACTIVO · DURACIÓN RECOMENDADA: 10-20 min

### Qué es
Conexión del material procesado con el corpus existente. Aquí
rag.py hace su trabajo: encontrar qué documentos del corpus tienen
score BM25 relevante para el nuevo conocimiento.

### Comandos IMV en fase RELATE
```bash
# Búsqueda RAG directa sobre el tema
cd ~/DIRIME/IMV && python3 -c "
import sys; sys.path.insert(0, '.')
from core.rag import search, build_full_index
build_full_index()
query = '[TEMA DE LA SEMANA]'
results = search(query, top_k=5)
for r in results:
    print(f'{r[\"score\"]:.2f}  {r[\"file\"]}')
    print(f'     {r[\"text\"][:100]}')
    print()
"

# Verificar si el tema ya está en cristales
python3 -c "
import sys; sys.path.insert(0, '.')
from core.ledger import get_verb_frequency
verbos = get_verb_frequency(30)
for v in verbos:
    if '[verbo_relevante]' in v['verb'].lower():
        print(v)
"
```

### Mapa de conexiones esperadas por biblioteca
```
Si el material es de TRUST  → buscar: COGNITIVOS · BIBLIO-SOURCES(TRUST*)
Si el material es de METHOD → buscar: UNICODE_METHOD* · grammar.py METHOD ops
Si el material es de SAMU   → buscar: BIBLIO-SOURCES(SAMU*) · samu.py
Si el material es de CRYPTO → buscar: MICRO_CRYPTO_ASIENTOS · UNICODE_BOLIVAR*
Si el material es de STACKING → buscar: cristales actuales · ledger.py
Si el material es de SOCIAL → buscar: MICRO_SOCIAL_COMPONENTES · Nerve Cells
Si es NOTARIA               → buscar: UNICODE_NOTARIA* · ballpaper.py
Si es KALIL                 → buscar: KALIL-NODOS-LACHO · UNICODE_PROGRAMS_KALIL*
```

### Señal de RELATE completo
El operador encontró ≥ 2 documentos con score BM25 > 1.0 y puede
articular cómo el nuevo material los complementa o contradice.

```
LACHO: STACKING UF[H48] =><= .. relaciona .. relate_score_bm25_corpus_conectado --[Nudo de Ocho] [term]
```

====================================================================
## FASE 4 — REAP · 數 WU · DURACIÓN: hasta cristalizar

### Qué es
La materialización soberana. El conocimiento verificado se convierte
en archivo, código, sentencia o cristal — algo que persiste en el
sistema y puede ser recuperado por RAG en sesiones futuras.

### Tipos de REAP en DIRIME
```
TIPO A — Archivo de corpus:
  Destino: ~/DIRIME/CORPUS/UNICODE PROGRAMS/UNICODE_*.txt
  Requiere: 4 anclas RAG al final
  Activa: RAG indexación en próximo build_full_index()

TIPO B — Código Python:
  Destino: ~/DIRIME/IMV/core/*.py o ~/DIRIME/tools/*.py
  Requiere: tests correspondientes en test_imv.py
  Activa: pytest · Scalar S verification

TIPO C — Nerve Cell:
  Destino: ~/DIRIME/RUNTIME/NERVE_CELLS/$dia.*.txt
  Requiere: sentencias LACHO VALID · anclas RAG × 4
  Activa: RAG indexación con boost nerve_cell × 2.0

TIPO D — Cristal directo:
  Comando: record_crystal() en ledger.py
  Requiere: verbo soberano · frecuencia verificada
  Activa: auto_crystallize() threshold check

TIPO E — Lacho file:
  Destino: ~/DIRIME/CONTROL/
  Requiere: sentencias VALID · generator --mode notaria si aplica
  Activa: RAG indexación · ledger TX
```

### Comandos IMV en fase REAP
```bash
# Verificar que el archivo creado es indexable
cd ~/DIRIME/IMV && python3 -c "
import sys; sys.path.insert(0, '.')
from core.rag import build_full_index, search
n, b = build_full_index()
print(f'docs: {n} · patrones: {b}')
r = search('[término del material reapado]', top_k=3)
for x in r: print(x['file'], round(x['score'],2))
"

# Verificar Scalar S post-REAP
python3 main.py --stats | grep "Scalar S"

# Confirmar cristales
python3 main.py --cristales | tail -5
```

### Checklist REAP
```
[ ] Archivo creado con path correcto (ubicaciones canónicas)
[ ] 4 anclas RAG al final si es .txt de corpus
[ ] Tests corren sin regresión: pytest tests/ -v | tail -3
[ ] RAG indexa el nuevo archivo con score > 0
[ ] Scalar S estable o mejoró post-REAP
[ ] LOG_PERMANENTE actualizado si es hito mayor
[ ] github_sync.sh ejecutado
```

### Señal de REAP completo
```bash
# Todos verdes:
cd ~/DIRIME/IMV && python3 -m pytest tests/ -v 2>&1 | tail -3
# Scalar S no bajó:
python3 main.py --stats | grep "Scalar S"
# El archivo es recuperable:
python3 -c "from core.rag import search; r=search('[tema]',top_k=1); print(r[0]['file'] if r else 'NOT FOUND')"
```

```
LACHO: STACKING UF[H63] =><= .. cristaliza .. reap_archivo_indexado_scalar_verificado --[Nudo de Ocho] [term]
```

====================================================================
## CICLO COMPLETO — EJEMPLO REAL: W13 METHOD × 4 NEURONAS

```
STRATEGIC ABSORPTION ($thu 19/03 mañana):
  "Absorber METHOD × 4 NEURONAS para mapear los 5 operadores
  formales a las 4 neuronas del sistema y aumentar coherencia"
  TRUST [scope] =><= .. declara .. sa_method_4_neuronas_w13 --[NdO] [term]

READ (1h):
  Leer: $thu 19-03 to $wed 25-03 completo
  Leer: BIBLIO-SOURCES(METHOD).txt en CORPUS/BIBLIA/
  Leer: grammar.py sección METHOD (Library.METHOD)
  → Registrar: "METHOD tiene 5 operadores · scalar_min=0.88 · level=1"

REFLECT (30min):
  1. Biblioteca principal: METHOD
  2. Cristal relacionado: buscar "calcula" "opera" en cristales
  3. Test que podría fallar: test_grammar_9_bibliotecas
  4. Pendiente que resuelve: S5.1 METHOD × 4 NEURONAS
  5. Scalar S requerido: 0.88 (scalar_min METHOD)
  → Tensión: ¿cómo mapeo <psi_spin> a HOUSE DRONE sin inventar?

RELATE (20min):
  search("METHOD equation operator_flow stat_onto psi_spin")
  → Resultado esperado: BIBLIO-SOURCES(METHOD_EQUATION) score alto
  → Resultado esperado: UNICODE DEEP LEARNING GUI score medio
  → Conecta con: COGNITIVO_03 TENER (inventario existente)

REAP ($thu + $fri + $sat · 12 tareas):
  → TIPO A: CORPUS/UNICODE PROGRAMS/UNICODE_METHOD_4_NEURONAS.txt
  → TIPO C: $thu.Nerve Cell METHOD Training.txt
  → TIPO B: grammar.py diff si hay extensión (diff mínimo)
  → Verificar: pytest 50+ · S=0.820+ · cristales=60+
```

====================================================================
## ANCLAS RAG × 4

GATE UF[H05] =><= .. espera .. read_mu_completo_antes_de_reflect --[Nudo Corredizo] [term]
SAMU @ =><= .. audita .. reflect_5_preguntas_ku_procesamiento --[Ballestrinque] [term]
STACKING UF[H48] =><= .. relaciona .. relate_bm25_corpus_conectado --[Nudo de Ocho] [term]
STACKING UF[H63] =><= .. cristaliza .. reap_wu_archivo_indexado_verificado --[Nudo de Ocho] [term]

[term] :: activo · [seal of secrecy] :: activo · 空聽數
