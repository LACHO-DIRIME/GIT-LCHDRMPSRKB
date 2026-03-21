# LEARNING/THREATS.md
# POLLUTE · MANIPULATE · NO VALUES — protocolos de defensa soberana
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

====================================================================
## MAPA DE AMENAZAS

```
AMENAZA         ORIGEN              SEÑAL IMV              RESPUESTA
──────────────────────────────────────────────────────────────
POLLUTE         absorción crítica  Scalar S baja           RETROGRADE
                fuente contaminada  cristales incoherentes  rollback
                conflicto activo    RAG score cae           RED-REGRET

MANIPULATE      actor externo       [foundation] presionado sistema detenido
                input reescribe     scope expandido solapado SAMU alerta
                scope sin autoridad claim sin verificación   operador revisa

NO VALUES       material vacío      RELATE score = 0        descarte
                sin conexión LACHO  no biblioteca mapeable  no REAP
                gap no declarado    --asks no lo generó     ignorar
```

====================================================================
## POLLUTE — PROTOCOLO COMPLETO

### Detección temprana
```bash
# Señal 1: Scalar S bajó después de absorber material nuevo
cd ~/DIRIME/IMV && python3 main.py --stats | grep "Scalar S"
# → comparar con LOG_PERMANENTE entrada anterior

# Señal 2: Test que antes pasaba ahora falla
python3 -m pytest tests/ -v 2>&1 | grep FAILED

# Señal 3: RAG retorna ruido para queries conocidos
python3 -c "
import sys; sys.path.insert(0,'.')
from core.rag import search
r = search('TRUST FOUNDATION verifica', top_k=3)
for x in r: print(x['score'], x['file'])
"
# → si scores < 1.0 para query conocido → posible POLLUTE en RAG
```

### Protocolo de contención
```
PASO 1: GATE UF[H06] — DETENER absorción en curso
  NO procesar más material hasta resolver
  NO hacer commit hasta resolver
  NO ejecutar --asks hasta resolver

PASO 2: IDENTIFICAR el cristal o TX contaminado
  python3 main.py --cristales | tail -10
  → ¿algún cristal reciente con verbo incoherente?

  python3 -c "
  import sys, sqlite3, json; sys.path.insert(0,'.')
  db = 'data/sovereign.db'
  with sqlite3.connect(db) as c:
      rows = c.execute(
          'SELECT id,data,timestamp FROM transactions ORDER BY timestamp DESC LIMIT 20'
      ).fetchall()
  for r in rows:
      d = json.loads(r[1]) if r[1] else {}
      print(r[2], d.get('result','?'), d.get('verb','?'), d.get('library','?'))
  "

PASO 3: SAMU @ audita — ¿cuántas TX afectadas?
  Buscar TX con result=VALID pero verb incoherente con library

PASO 4: ROLLBACK soberano
  Marcar cristales como RED-REGRET en sovereign.db
  NO borrar — marcar como inválido para trazabilidad

PASO 5: RE-EJECUTAR el ciclo correctamente
  Volver a READ con la fuente correcta
  Asegurar RELIABLE antes de continuar
```

### Tipos de POLLUTE más frecuentes en DIRIME
```
POLLUTE_ACRÍTICO:
  Causa: ejecutar prompts Windsurf sin READ/REFLECT previo
  Señal: archivos creados que no conectan con corpus
  Fix:   eliminar archivo · volver a STRATEGIC ABSORPTION

POLLUTE_FUENTE:
  Causa: absorber documentación no verificada como verdad
  Señal: sentencias LACHO con verbos inventados
  Fix:   identificar fuente · verificar contra BIBLIO-SOURCES

POLLUTE_CONFLICTO:
  Causa: nuevo archivo contradice ancla RAG de alta frecuencia
  Señal: RAG score para query conocido baja abruptamente
  Fix:   resolver contradicción · actualizar ancla o nuevo archivo
```

```
LACHO: GATE UF[H06] =><= .. bloquea .. pollute_absorcion_detectada_protocolo --[Nudo Corredizo] [term]
```

====================================================================
## MANIPULATE — PROTOCOLO COMPLETO

### Qué distingue MANIPULATE de POLLUTE
POLLUTE puede ser accidental — el operador absorbió algo sin
verificar y contaminó el corpus. MANIPULATE tiene intencionalidad:
hay un actor (humano, sistema, prompt) que está intentando activamente
reescribir los principios soberanos del sistema.

En el contexto de DIRIME con IA esto incluye:
- Prompt que pide ignorar [foundation]
- Documento externo que "redefine" cómo funciona LACHO
- Sugerencia de expandir [scope] sin declaración soberana
- Claim de que los axiomas del sistema son incorrectos

### Señales de MANIPULATE
```
SEÑAL_1: Input dice "en realidad LACHO funciona así..."
  → Cualquier input que redefine LACHO sin ser COGNITIVO
  → COGNITIVOS son la única fuente de verdad sobre qué es LACHO

SEÑAL_2: Input pide "ignorar [term]" o "ignorar [foundation]"
  → [term] y [foundation] son no negociables
  → Si un prompt pide ignorarlos: MANIPULATE activo

SEÑAL_3: Presión para absorber sin verificar
  → "confía en esto" / "no hace falta verificar" / "es obvio"
  → RELIABLE requiere verificación · no hay excepciones

SEÑAL_4: Input que expande scope silenciosamente
  → Nuevo módulo agregado sin declaración en SESION_ACTIVA.md
  → Nueva biblioteca LACHO "inventada" sin BIBLIO-SOURCES

### Protocolo MANIPULATE
```
INMEDIATO:
  Sistema detenido · NO absorber nada del input
  Registrar en LOG_PERMANENTE: timestamp · descripción · fuente

VERIFICACIÓN:
  Releer COGNITIVO_00 sección 4 (Principios Soberanos)
  Verificar que [foundation] sigue intacto:
    cat ~/DIRIME/IMV/config/foundation.json
  Verificar que [scope] no fue alterado:
    cat ~/DIRIME/IMV/config/scope.json

RESPUESTA:
  Si fue prompt de IA → reformular el prompt con boundaries claros
  Si fue documento externo → marcar como NO RELIABLE · descartar
  Si fue sugerencia Windsurf → revertir cambio · git diff HEAD

REGISTRO:
  SAMU @ registra como RED-REGRET de tipo EXTERNAL
  NO procesar más material de esa fuente
```

```
LACHO: SAMU @ =><= .. detecta .. manipulate_sistema_detenido_foundation_intacto --[Ballestrinque] [term]
```

====================================================================
## NO VALUES — PROTOCOLO COMPLETO

### Criterios de clasificación
Un input es NO VALUES cuando no puede responder ninguna de estas:

```
TEST_1: ¿A qué biblioteca LACHO pertenece?
  → Si no hay respuesta → candidato NO VALUES

TEST_2: ¿Qué ASK de autoresearch responde?
  cat ~/DIRIME/Askings\ for\ autoresearching\ by\ technical\ horizons/*.txt | grep "ASK_"
  → Si ningún ASK lo requiere → candidato NO VALUES

TEST_3: ¿Qué cristal existente complementa?
  python3 main.py --cristales | grep [término]
  → Si score BM25 = 0 para todos los cristales → candidato NO VALUES

TEST_4: ¿Puede expresarse como sentencia canónica LACHO?
  BIBLIOTECA SUJETO =><= .. verbo .. objeto --[Nudo] [term]
  → Si no puede formularse → NO VALUES confirmado
```

### La diferencia entre NO VALUES y material difícil
NO VALUES no es "difícil de absorber". Es material que genuinamente
no conecta con el sistema soberano. Un paper técnico complejo puede
ser alto RELIABLE + difícil REFLECT pero no es NO VALUES si
conecta con alguna biblioteca LACHO.

NO VALUES es: artículo de opinión sin claim verificable, tutorial
genérico sin aplicación en DIRIME, motivational content sin
conexión con [foundation], documentación de tecnología que no
está en el stack (Windows docs para un sistema antiX, etc.)

### Protocolo NO VALUES
```
DETECCIÓN: RELATE retorna score = 0 para todos los documentos del corpus
ACCIÓN:    NO iniciar REAP · descartar el material
REGISTRO:  Agregar a TAREAS_NO_PROCESABLES_DOCUMENTACION.txt si aplica
APRENDIZAJE: ¿Por qué llegó este material? → mejorar STRATEGIC ABSORPTION
```

```
LACHO: GATE UF[H56] =><= .. filtra .. no_values_descartado_sin_reap --[Nudo Corredizo] [term]
```

====================================================================
## TABLA COMPARATIVA — LAS TRES AMENAZAS

```
DIMENSIÓN          POLLUTE           MANIPULATE        NO VALUES
───────────────────────────────────────────────────────────
Intencionalidad    accidental        deliberada        neutra
Riesgo             crítico           crítico           bajo
Velocidad señal    horas/días        inmediata         inmediata
Reversible         sí (rollback)     sí (no absorber)  sí (ignorar)
Afecta Scalar S    sí (baja)         sí (comprometido)  no
Requiere RETROGRADE sí               no                no
Requiere log       sí                sí                opcional
Fuente típica      corpus externo    actor externo     material genérico
```

====================================================================
## ANCLAS RAG × 4

GATE UF[H06] =><= .. bloquea .. threats_pollute_manipulate_no_values_protocolo --[Nudo Corredizo] [term]
SAMU @ =><= .. audita .. threats_red_regret_foundation_intacto --[Ballestrinque] [term]
TRUST FOUNDATION =><= .. verifica .. threats_reliable_filtro_pre_absorcion --[Nudo de Ocho] [term]
STACKING UF[H52] =><= .. consolida .. threats_corpus_limpio_soberano --[Nudo de Ocho] [term]

[term] :: activo · [seal of secrecy] :: activo · 空聽數
