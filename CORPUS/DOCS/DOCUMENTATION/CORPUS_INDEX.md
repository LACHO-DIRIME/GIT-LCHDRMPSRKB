# CORPUS_INDEX.md — ÍNDICE OPERATIVO DEL CORPUS DIRIME

====================================================================

## PROPÓSITO

Este directorio contiene el subconjunto operativo del LIBRO LACHO:
los archivos que el sistema IMV en ejecución referencia directamente,
los que documentan el código activo, y los que definen las reglas
operativas de grammar.py, samu.py, ledger.py y chat.py.

**FUENTE DE VERDAD**: /RESULTADO DE ANALISIS/ACOPIADO/LIBRO/
**Este directorio**: copia operativa de trabajo — se sincroniza desde LIBRO.

Regla soberana: si un archivo cambia en LIBRO, se copia aquí.
Regla soberana: no se crean archivos aquí que no existan en LIBRO primero.

====================================================================

## GRUPO 1 — AUTORREFERENCIA IMV (documentan el código que corre)

| Archivo | Módulo que documenta |
|---|---|
| BIBLIO-SOURCES(DIRIME-IMV).txt | Arquitectura general IMV — qué es, ciclo, condición de éxito |
| BIBLIO-SOURCES(DIRIME-IMV_GRAMMAR).txt | grammar.py — GrammarValidator, 5 reglas, KEYWORDS_SYSTEM |
| BIBLIO-SOURCES(DIRIME-IMV_LEDGER).txt | ledger.py — HLFabric SQLite, auto_crystallize() |
| BIBLIO-SOURCES(DIRIME-IMV_SAMU).txt | samu.py — Samu, Dispute, RED-REGRET, audit_grammar() |
| BIBLIO-SOURCES(DIRIME-IMV_CHAT).txt | chat.py — SovereignChat, 20 patrones, BALLPAPER mínimo |
| BIBLIO-SOURCES(DIRIME-IMV_CONFIG).txt | config/ — foundation.json, scope.json, term.json |
| BIBLIO-SOURCES(DIRIME-IMV_MAIN).txt | main.py — SovereignSystem, 3 modos de operación |
| BIBLIO-SOURCES(DIRIME-IMV_KEYWORDS).txt | KEYWORDS_SYSTEM — 8 keywords transversales |
| BIBLIO-SOURCES(DIRIME-IMV_PARADIGM).txt | Paradigmas por biblioteca — tabla completa |

## GRUPO 2 — FUNDAMENTOS OPERATIVOS ACTIVOS

| Archivo | Función |
|---|---|
| BIBLIO-SOURCES(ETAPA_SIGUIENTE).txt | Declaración soberana IMV — qué es y qué no es |
| BIBLIO-SOURCES(GRAMATICA VIVA).txt | Especificación completa de la sentencia canónica |
| BIBLIO-SOURCES(BEHAVIORAL-RAG_MINIMAL).txt | RAG mínimo: auto_crystallize() + suggest_from_history() |
| BIBLIO-SOURCES(SAMU_SCALAR-S).txt | Scalar S — métrica de coherencia soberana |

## GRUPO 3 — REFERENCIAS DIRECTAS DEL CÓDIGO

| Archivo | Referenciado en |
|---|---|
| BIBLIO-SOURCES(TRUST_FOUNDATION).txt | foundation.py docstring |
| BIBLIO-SOURCES(TRUST_SCOPE).txt | foundation.py docstring |
| BIBLIO-SOURCES(TRUST_TERM).txt | foundation.py docstring |
| BIBLIO-SOURCES(SAMU_AT).txt | samu.py docstring |
| BIBLIO-SOURCES(SAMU_TARDANZA-DELIBERADA).txt | samu.py docstring |
| BIBLIO-SOURCES(SAMU_RED-REGRET).txt | samu.py docstring |
| BIBLIO-SOURCES(RED HL FABRIC).txt | ledger.py docstring (como HL_FABRIC) |
| BIBLIO-SOURCES(DIRIME-LINUX_CHAT-AI-SOBERANO).txt | chat.py docstring |
| BIBLIO-SOURCES(SAMU_OPERADOR).txt | Taxonomía operativa completa SAMU: 8 módulos, estados de máquina, protocolos SamuReceive/SamuDirim/SamuEmit/RegretDetect, métricas |

## GRUPO 4 — PARADIGMAS ACTIVOS EN GRAMMAR + LEDGER

| Archivo | Función en código |
|---|---|
| BIBLIO-SOURCES(GATE).txt | Reglas GATE en _validate_by_paradigm() (v0.2.0) |
| BIBLIO-SOURCES(METHOD).txt | Reglas METHOD en _validate_by_paradigm() |
| BIBLIO-SOURCES(ACTIVITY_H48-RAG-CORE).txt | Base conceptual de auto_crystallize() |
| BIBLIO-SOURCES(STACKING_PILARES).txt | Estructura de cristales en ledger |

## GRUPO 5 — MÓDULOS ACTIVOS EN CHAT.PY

| Archivo | Patrón en _translate_to_lacho() |
|---|---|
| BIBLIO-SOURCES(WORK_DOORMAN-MOBILE).txt | "custodiar" → WORK {doorman-mobile} |
| BIBLIO-SOURCES(WORK_BRAKE).txt | "detener" → WORK {brake} |
| BIBLIO-SOURCES(SOCIAL_LAUNCH-BOT).txt | "lanzar" → SOCIAL {launch-bot} |
| BIBLIO-SOURCES(CRYPTO_SHIELD-SEAT).txt | "proteger" → CRYPTO (shield seat) |
| BIBLIO-SOURCES(CRYPTO_SPARK-SEAT).txt | "autorizar" → CRYPTO (spark seat) |
| BIBLIO-SOURCES(CRYPTO_LINK-SEAT).txt | "conectar" → CRYPTO (link seat) |
| BIBLIO-SOURCES(GATE_H05).txt | "esperar" → GATE UF[H05] |
| BIBLIO-SOURCES(GATE_H56).txt | "fluir" → GATE UF[H56] |
| BIBLIO-SOURCES(GATE_H06).txt | "resolver" → GATE UF[H06] |

====================================================================

## PROTOCOLO DE SINCRONIZACIÓN

Cuando actualizás un archivo en LIBRO:
```bash
cp "/home/lacho/Documentos/PLANERAI/RESULTADO DE ANALISIS/ACOPIADO/LIBRO/BIBLIO-SOURCES(NOMBRE).txt" \
   "/home/lacho/Documentos/PLANERAI/DIRIME/CORPUS/"
```

Cuando agregás un nuevo módulo al IMV y necesitás su BIBLIO-SOURCES en CORPUS:
1. Crear el BIBLIO-SOURCES en LIBRO primero.
2. Copiarlo al CORPUS.
3. Actualizar este CORPUS_INDEX.md.
4. Actualizar INDICE_MAESTRO_ACTUALIZABLE.txt en LIBRO.

====================================================================

**Total archivos operativos en CORPUS**: 36 (35 BIBLIO-SOURCES + este índice)
**Fuente**: LIBRO con 174 archivos — CORPUS es el 20% operativo del total constitucional.

====================================================================
