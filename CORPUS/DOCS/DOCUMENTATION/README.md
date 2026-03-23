# CORPUS — Subconjunto Operativo del LIBRO LACHO

## 📖 Propósito

Este directorio contiene el subconjunto operativo del LIBRO LACHO: los archivos que el sistema IMV en ejecución referencia directamente, los que documentan el código activo, y los que definen las reglas operativas de grammar.py, samu.py, ledger.py y chat.py.

**FUENTE DE VERDAD**: `/RESULTADO DE ANALISIS/ACOPIADO/LIBRO/` (175 archivos)  
**ESTE DIRECTORIO**: Copia operativa de trabajo — se sincroniza desde LIBRO (36 archivos).

## 🔄 Protocolo de Sincronización

### Regla soberana #1
Si un archivo cambia en LIBRO, se copia aquí:
```bash
cp "/RESULTADO DE ANALISIS/ACOPIADO/LIBRO/BIBLIO-SOURCES(NOMBRE).txt" "./CORPUS/"
```

### Regla soberana #2
No se crean archivos aquí que no existan en LIBRO primero.

### Regla soberana #3
Cuando se agrega un nuevo módulo al IMV:
1. Crear BIBLIO-SOURCES en LIBRO primero
2. Copiarlo al CORPUS
3. Actualizar CORPUS_INDEX.md
4. Actualizar INDICE_MAESTRO_ACTUALIZABLE.txt

## 📚 Contenido Operativo

### GRUPO 1 — Autorreferencia IMV (9 archivos)
Documentan el código que corre hoy:
- `DIRIME-IMV` — Arquitectura general
- `DIRIME-IMV_GRAMMAR` — grammar.py completo
- `DIRIME-IMV_LEDGER` — ledger.py + HL FABRIC
- `DIRIME-IMV_SAMU` — samu.py + Scalar S
- `DIRIME-IMV_CHAT` — chat.py + 4 niveles
- `DIRIME-IMV_CONFIG` — config/ externo
- `DIRIME-IMV_MAIN` — main.py orquestador
- `DIRIME-IMV_KEYWORDS` — 8 keywords transversales
- `DIRIME-IMV_PARADIGM` — tabla paradigmas

### GRUPO 2 — Fundamentos Operativos (4 archivos)
Referenciados por código o inmediatos:
- `ETAPA_SIGUIENTE` — Declaración IMV
- `GRAMATICA VIVA` — Especificación sentencia
- `BEHAVIORAL-RAG_MINIMAL` — RAG mínimo
- `SAMU_SCALAR-S` — Métrica coherencia

### GRUPO 3 — Referencias Directas (9 archivos)
Aparecen en docstrings del código:
- `TRUST_FOUNDATION/SCOPE/TERM` — foundation.py
- `SAMU_AT/TARDANZA-DELIBERADA/RED-REGRET` — samu.py
- `RED HL FABRIC` — ledger.py
- `DIRIME-LINUX_CHAT-AI-SOBERANO` — chat.py
- `SAMU_OPERADOR` — Taxonomía unificada

### GRUPO 4 — Paradigmas Activos (4 archivos)
Reglas operativas en grammar.py y ledger.py:
- `GATE` — Reglas GATE en _validate_by_paradigm()
- `METHOD` — Reglas METHOD
- `ACTIVITY_H48-RAG-CORE` — Base auto_crystallize()
- `STACKING_PILARES` — Estructura cristales

### GRUPO 5 — Módulos en chat.py (9 archivos)
20 patrones del traductor:
- `WORK_DOORMAN-MOBILE/BRAKE` — "custodiar"/"detener"
- `SOCIAL_LAUNCH-BOT` — "lanzar"
- `CRYPTO_SHIELD-SEAT/SPARK-SEAT/LINK-SEAT` — "proteger"/"autorizar"/"conectar"
- `GATE_H05/H56/H06` — "esperar"/"fluir"/"resolver"

## 📖 Navegación

### CORPUS_INDEX.md
Mapa completo del corpus operativo con:
- Tablas por grupo y propósito
- Referencias cruzadas al código
- Protocolo de sincronización

### Referencias en Código
```python
# En docstrings de módulos:
"""
Referencia canónica:
  BIBLIO-SOURCES(TRUST_FOUNDATION).txt
"""
```

## 🎯 Uso Para Desarrollo

### Cuando trabajas en grammar.py
Consulta: `DIRIME-IMV_GRAMMAR.txt` + `GRAMATICA VIVA.txt` + `DIRIME-IMV_PARADIGM.txt`

### Cuando trabajas en samu.py
Consulta: `DIRIME-IMV_SAMU.txt` + `SAMU_SCALAR-S.txt` + `SAMU_OPERADOR.txt`

### Cuando trabajas en ledger.py
Consulta: `DIRIME-IMV_LEDGER.txt` + `RED HL FABRIC.txt` + `BEHAVIORAL-RAG_MINIMAL.txt`

### Cuando trabajas en chat.py
Consulta: `DIRIME-IMV_CHAT.txt` + `DIRIME-LINUX_CHAT-AI-SOBERANO.txt`

## 📊 Estadísticas

- **Total archivos operativos**: 36 (35 BIBLIO-SOURCES + CORPUS_INDEX.md)
- **Porcentaje del LIBRO**: 20% operativo del total constitucional
- **Última sincronización**: Ver .sovereign (CORPUS_LAST_SYNC)

## 🚨 Importante

### NO EDITAR DIRECTAMENTE AQUÍ
Los archivos aquí son copias. Las ediciones deben hacerse en LIBRO y luego sincronizarse.

### VERIFICAR INTEGRIDAD
```bash
# Contar archivos operativos:
ls CORPUS/ | grep -v ".gitkeep" | wc -l  # Debe ser 36

# Verificar que exista CORPUS_INDEX.md:
ls CORPUS/CORPUS_INDEX.md
```

### ACTUALIZAR .sovereign
Cuando se agrega un archivo, actualizar:
- `CORPUS_TOTAL` en .sovereign
- `CORPUS_LAST_SYNC` con fecha actual

## 🔗 Relación con LIBRO

```
LIBRO (175 archivos) → CORPUS (36 archivos) → CÓDIGO IMV
     ↓                    ↓                    ↓
Especificación     Subconjunto        Referencias
completa           operativo          directas
```

El CORPUS es el puente soberano entre la constitución completa (LIBRO) y la implementación verificable (código).

---

**Para agentes AI**: Este directorio contiene solo lo que el sistema IMV necesita para operar hoy. Para la especificación completa, consultar LIBRO. Para sincronizar cambios, siempre desde LIBRO → CORPUS.
