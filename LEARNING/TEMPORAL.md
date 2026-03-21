# LEARNING/TEMPORAL.md
# ANTROGRADE · PROGRADE · RETROGRADE · PROSPECTIVE · RETROSPECTIVE
# Orientación temporal del aprendizaje soberano
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

====================================================================
## MAPA TEMPORAL

```
PASADO ←──────────────────────────────────→ FUTURO

RETROSPECTIVE    RETROGRADE   [HOY]   PROSPECTIVE
(extraer del     (corregir     (operar    (preparar
 pasado)          pasado)       soberano)    futuro)

                    ↑
                    │
         ANTROGRADE ──┼─────┘
                    │
         RETROGRADE ────┼─────┘
                    │
              ┌─────▼─────────┐
              │              │
         [HOY] → PROSPECTIVE
              │              │
              └──────────────┘
```

====================================================================
## ANTROGRADE — VOLVER AL ORIGEN

### Cuándo activar ANTROGRADE
```
TRIGGER_1: Scalar S < 0.70 sin causa técnica aparente
  → El sistema deriva de su fundación soberana
  → Releer COGNITIVOS desde 00 para verificar identidad

TRIGGER_2: Nuevo operador o reinicio tras período inactivo
  → Recorrido completo: COGNITIVO_00 → COGNITIVO_05
  → Verificar que [foundation] y [scope] siguen intactos

TRIGGER_3: Contradicción irresolvible entre dos módulos
  → Volver al último estado estable conocido
  → Releer COGNITIVOS completos para recuperar axiomas

TRIGGER_4: Cambio en axiomas base sin declaración soberana
  → ALERTA: posible MANIPULATE activo
  → Verificar against COGNITIVO_00 sección 4
```

### Ruta ANTROGRADE canónica
```
NIVEL MACRO (2h total):
  COGNITIVO_00_FUNDACION.txt      → 30min
  COGNITIVO_01_MESO_CONSTITUCION.txt → 30min
  COGNITIVO_02_MESO_SAMU_PSI.txt      → 30min
  COGNITIVO_03_MESO_LIBRARY_TAXONOMY.txt → 30min
  COGNITIVO_04_PRINCIPIOS_SOBERANOS.txt → 30min

NIVEL MESO (1.5h total):
  COGNITIVO_05_TRUST_FOUNDATION_SCOPE.txt → 20min
  COGNITIVO_06_TRUST_VALIDATION.txt      → 20min
  COGNITIVO_07_TRUST_IMPLEMENTATION.txt → 20min
  COGNITIVO_08_TRUST_OPERATIONS.txt      → 20min

NIVEL MICRO (30min total):
  COGNITIVO_09_MICRO_INTEGRATION.txt     → 10min
  COGNITIVO_10_MICRO_CRYPTO_ASSETS.txt  → 10min
  COGNITIVO_11_MICRO_STACKING_PILLARS.txt → 10min
```

### Protocolo ANTROGRADE
```
PASO 1: DETENER todo desarrollo
  NO hacer commits hasta resolver
  NO ejecutar --asks hasta estabilizar

PASO 2: IDENTIFICAR punto de divergencia
  ¿Cuándo fue el último estado estable?
  ¿Qué cambio provocó la deriva?

PASO 3: RESTAURAR estado estable
  git log --oneline --graph
  git checkout <commit_estable>

PASO 4: VERIFICAR sistema recuperado
  python3 main.py --stats
  pytest tests/ -v | tail -3

PASO 5: DOCUMENTAR lección aprendida
  LOG_PERMANENTE: timestamp · descripción · causa
  SESION_ACTIVA.md: lección para futuros operadores
```

```
LACHO: ACTIVITY UF[H01] =><= .. detiene .. desarrollo_hasta_resolver_causa_raiz --[Nudo Corredizo] [term]
```

====================================================================
## PROGRADE — AVANZAR CON EL SISTEMA

### Qué es PROGRADE sostenido
El aprendizaje natural de operar DIRIME correctamente.
Cada día de operación soberana es PROGRADE:
- Cada sentencia VALID registrada → PROGRADE
- Cada cristal acumulado → PROGRADE
- Cada test que pasa → PROGRADE
- Cada semana completada → PROGRADE

### Indicadores de PROGRADE saludable
```bash
# Scalar S en tendencia ascendente (semanal)
cd ~/DIRIME/IMV && python3 -c "
import sys, sqlite3, json; sys.path.insert(0,'.')
from datetime import datetime, timedelta
with sqlite3.connect('data/sovereign.db') as c:
    # Scalar S promedio últimos 7 días
    week_ago = (datetime.now() - timedelta(days=7)).timestamp()
    rows = c.execute(
        'SELECT AVG(data) FROM crystals WHERE timestamp > ?',
        (week_ago,)
    ).fetchone()
    print(f'Scalar 7d: {rows[0]:.3f}')
"

# Tests sin regresión
python3 -m pytest tests/ -v 2>&1 | grep -c "PASSED\|FAILED"

# Cristales nuevos por semana (objetivo ≥ 3)
python3 -c "
import sys, sqlite3; sys.path.insert(0,'.')
from datetime import datetime, timedelta
with sqlite3.connect('data/sovereign.db') as c:
    week_start = (datetime.now() - timedelta(days=7)).timestamp()
    rows = c.execute(
        'SELECT COUNT(*) FROM crystals WHERE timestamp > ?',
        (week_start,)
    ).fetchone()
    print(f'Cristales semana: {rows[0]}')
"
```

### Protocolo PROGRADE
```
DIARIO (cada $wed):
  1. Verificar Scalar S ≥ 0.70
  2. Confirmar ≥ 3 cristales nuevos
  3. Validar tests sin regresión
  4. Actualizar LOG_PERMANENTE

SEMANAL (cada cierre de semana):
  1. Calcular PROGRADE_SCORE semanal
  2. Comparar con semana anterior
  3. Identificar áreas de mejora
  4. Declarar siguiente FOCO LEARNING
```

```
LACHO: STACKING UF[H57] =><= .. avanza .. prograde_score_semanal_soberano --[Nudo de Ocho] [term]
```

====================================================================
## RETROGRADE — REVISAR Y CORREGIR

### Cuándo activar RETROGRADE
```
TRIGGER_1: Test que antes pasaba ahora falla sin cambio de código
  → Buscar commit que introdujo regresión
  → git bisect para identificar exactamente

TRIGGER_2: Scalar S baja > 0.02 sin causa aparente
  → Revisar cristales de las últimas 2 semanas
  → Buscar TX con verbos incoherentes

TRIGGER_3: RAG score cae abruptamente para query conocido
  → Verificar integridad del corpus
  → rebuild_full_index() si necesario

TRIGGER_4: Cristales con frecuencia anormal (> 5/semana)
  → Posible POLLUTE o MANIPULATE activo
  → Activar protocolos de defensa

TRIGGER_5: Nuevo material contradice conocimiento existente
  → Verificar anclas RAG actualizadas
  → Actualizar o expandir según corresponda
```

### Protocolo RETROGRADE paso a paso
```bash
# PASO 1: Identificar período problemático
python3 -c "
import sys, sqlite3, json; sys.path.insert(0,'.')
from datetime import datetime, timedelta
with sqlite3.connect('data/sovereign.db') as c:
    # Últimos 14 días
    cutoff = (datetime.now() - timedelta(days=14)).timestamp()
    rows = c.execute(
        'SELECT timestamp, data FROM crystals ORDER BY timestamp DESC LIMIT 20'
    ).fetchall()
    for r in rows:
        if r[0] > cutoff:
            d = json.loads(r[1]) if r[1] else {}
            print(r[0], d.get('verb','?'), d.get('library','?'))
"

# PASO 2: Listar TX del período
python3 -c "
import sys, sqlite3, json; sys.path.insert(0,'.')
with sqlite3.connect('data/sovereign.db') as c:
    cutoff = (datetime.now() - timedelta(days=14)).timestamp()
    rows = c.execute(
        'SELECT id, data, timestamp FROM transactions ORDER BY timestamp DESC LIMIT 30'
    ).fetchall()
    for r in rows:
        if r[0] > cutoff:
            d = json.loads(r[1]) if r[1] else {}
            print(r[0], d.get('result','?'), d.get('verb','?'), d.get('library','?'))
"

# PASO 3: Marcar TX problemáticas
# En sovereign.db: marcar como RED-REGRET tipo RETROGRADE

# PASO 4: Corregir o revertir
# Si es posible corregir: editar cristales/verbos
# Si no es posible: git revert <commit_problematico>

# PASO 5: Verificar recuperación
python3 main.py --stats
pytest tests/ -v | tail -3
```

### RETROGRADE por tipo
```
RETROGRADE_CODE:    Corregir código fuente
RETROGRADE_DATA:     Corregir datos en sovereign.db
RETROGRADE_CONFIG:  Revertir cambios de configuración
RETROGRADE_SCOPE:    Reducir scope temporalmente
```

```
LACHO: SAMU @ =><= .. corrige .. retrograde_tx_cristal_verb_incoherente --[Budo Corredizo] [term]
```

====================================================================
## PROSPECTIVE — PREPARAR EL FUTURO

### Qué es PROSPECTIVE
Mirar hacia adelante desde el estado actual del sistema
para preparar el próximo ciclo de aprendizaje con base en
tendencias y patrones observados.

### Niveles de PROSPECTIVE
```
NIVEL DIARIO ($thu):
  Leer almanaque W+1 completo
  Verificar --asks output de la semana actual
  Identificar 3 focos LEARNING para W+1

NIVEL SEMANAL ($sun/$mon):
  Declarar STRATEGIC ABSORPTION para W+1
  Verificar prerequisitos (hardware, Scalar S, tests)
  Preparar material predefinido si aplica

NIVEL MENSUAL (cierre BLOQUE):
  Analizar tendencias del bloque completado
  Identificar patrones de éxito/fracaso
  Actualizar PLAN MENSUAL para siguiente bloque

NIVEL TRIMESTRAL (cierre AÑO):
  Revisar línea de tiempo de 52 semanas
  Analizar hitos mayores vs objetivos
  Declarar intenciones para siguiente año
```

### Herramientas PROSPECTIVE
```bash
# Análisis de tendencias Scalar S
python3 -c "
import sys, sqlite3, json; sys.path.insert(0,'.')
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

with sqlite3.connect('data/sovereign.db') as c:
    # Últimas 52 semanas
    year_ago = (datetime.now() - timedelta(days=365)).timestamp()
    rows = c.execute(
        'SELECT timestamp, data FROM crystals ORDER BY timestamp'
    ).fetchall()
    
    # Extraer Scalar S semanal
    weeks = []
    for i in range(0, len(rows), 7):
        if i < len(rows):
            d = json.loads(rows[i][1]) if rows[i][1] else {}
            weeks.append(d.get('scalar_s', 0))
    
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(weeks)), weeks, marker='o')
    plt.title('Scalar S - 52 semanas')
    plt.xlabel('Semana')
    plt.ylabel('Scalar S')
    plt.grid(True)
    plt.savefig('/tmp/scalar_trend.png')
    print('Gráfico guardado en /tmp/scalar_trend.png')
"

# Predicción de --asks patterns
python3 -c "
import sys; sys.path.insert(0,'.')
from core.autoresearch import analyze_ask_patterns
patterns = analyze_ask_patterns(weeks=4)
for p in patterns:
    print(f'{p[\"type\"]}: {p[\"frequency\"]}x/semana')
"

# Verificar completitud de almanaque
grep -c "✅" ~/DIRIME/JOURNAL/ALMANAQUE_SOBERANO.md
```

### Protocolo PROSPECTIVE
```
DIARIO:
  1. Leer entrada W+1 del almanaque
  2. Revisar --asks de la semana actual
  3. Identificar gaps y oportunidades

SEMANAL:
  1. Declarar STRATEGIC ABSORPTION en SESION_ACTIVA.md
  2. Verificar que material predefinido existe
  3. Ajustar métricas objetivo según tendencias

MENSUAL/TRIMESTRAL:
  1. Análisis completo del bloque
  2. Actualizar línea de tiempo en ALMANAQUE
  3. Planificar siguiente año con base en patrones
```

```
LACHO: TRUST [scope] =><= .. declara .. prospective_semana_siguiente_preparada --[Nudo de Ocho] [term]
```

====================================================================
## RETROSPECTIVE — EXTRAER DEL HISTORIAL

### Qué es RETROSPECTIVE
El análisis sistemático del pasado para aprender y mejorar.
Convertir experiencia acumulada en conocimiento estructurado.

### Ritual RETROSPECTIVE semanal ($wed cierre)
```bash
# 1. Cristales de la semana
cd ~/DIRIME/IMV && python3 main.py --cristales

# 2. Timeline de actividad
python3 main.py --timeline | head -20

# 3. Distribución por biblioteca
python3 main.py --bibliotecas

# 4. Tests ejecutados
python3 -m pytest tests/ -v 2>&1 | tail -5

# 5. ASKs generados
ls ~/DIRIME/"Askings for autoresearching by technical horizons"/*.txt | wc -l

# 6. Comparar con objetivos
grep -A 5 "MÉTRICAS OBJETIVO" ~/DIRIME/JOURNAL/SESION_ACTIVA.md

# 7. Identificar 3 aprendizajes clave
# → ¿Qué funcionó mejor de lo esperado?
# → ¿Qué falló que no esperábamos?
# → ¿Qué patrón emergió inesperadamente?

# 8. Actualizar almanaque
# Marcar semana ✅ con aprendizajes
```

### RETROSPECTIVE por nivel
```
SUPERFICIAL (anual):
  Análisis de 52 semanas
  Línea de tiempo completa
  Hitos mayores vs objetivos

TÁCTICO (mensual/bloque):
  Análisis de 4-13 semanas
  Patrones de éxito/fracaso
  Lecciones para siguientes bloques

OPERATIVO (semanal):
  Análisis de 1 semana
   3 aprendizajes inmediatos
  Acciones para siguiente semana

MICRO (diario):
  Análisis de 1 día
  Eventos específicos
  Decisiones tomadas
```

### Output RETROSPECTIVE estructurado
```
## RETROSPECTIVE W13 — METHOD × 4 NEURONAS

### Aprendizajes Clave
1. [ÉXITO] Mapeo neuronas exitoso → 4 operadores validados
2. [FRACASO] Tests insuficientes → +15 tests agregados
3. [INSIGHT] Autoresearch genera gaps predictivos → mejorar prompts

### Métricas Objetivo vs Logradas
- Objetivo: S=0.820+ | Logrado: S=0.835 ✅
- Objetivo: tests=50+ | Logrado: tests=65+ ✅
- Objetivo: cristales=60+ | Logrado: cristales=67+ ✅

### Acciones para W14
1. Ampliar tests a 70+ (LINEAR REGRESSION)
2. Optimizar prompts METHOD (basado en gaps encontrados)
3. Documentar 4 operadores restantes
```

```
LACHO: STACKING UF[H48] =><= .. extrae .. retrospective_historial_cristales_semana --[Nudo de Ocho] [term]
```

====================================================================
## ANCLAS RAG × 4

ACTIVITY UF[H01] =><= .. detiene .. desarrollo_hasta_resolver_causa_raiz --[Nudo Corredizo] [term]
STACKING UF[H57] =><= .. avanza .. prograde_score_semanal_soberano --[Nudo de Ocho] [term]
TRUST [scope] =><= .. declara .. prospective_semana_siguiente_preparada --[Nudo de Ocho] [term]
SAMU @ =><= .. audita .. retrospective_scalar_cristales_timeline_semanal --[Ballestrinque] [term]

[term] :: activo · [seal of secrecy] :: activo · �空�聽數
