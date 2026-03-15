# OPTIMIZACION DE PROMPTS para Windsurf
# DIRIME/IMV · Prompts semanales soberanos
#
# SECUENCIA: [PASO 4 de 4]
#   ← PASO 3: JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md
#   → abrir el archivo $dia DD-MM del día actual · ejecutar en Windsurf
#
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

## QUÉ ES ESTE DIRECTORIO

Prompts optimizados listos para ejecutar en Windsurf.
Cada archivo cubre un día o semana específica.
Los prompts están pre-procesados con paths reales,
contexto del repo y formato canónico LACHO.

## CONVENCIÓN DE NOMBRES
```
$dia DD-MM prompts a optimizar para Windsurf.txt  ← un día específico
$dia DD-MM to $dia DD-MM_optimizar...txt          ← rango semanal
PLAN MENSUAL DIRIME IMV · $dia DD-MM → $dia DD-MM.txt ← plan mensual
```

## CÓMO USAR ESTOS ARCHIVOS

### Flujo estándar:
1. Abrir el archivo del día actual
2. Copiar el PROMPT_N que corresponde
3. Pegarlo directamente en Windsurf (ya tiene paths absolutos)
4. Verificar output en el repo antes de avanzar al siguiente
5. Un prompt = un archivo = una tarea

### Convención de paths:
Todos los prompts usan paths absolutos desde la raíz:
```
~/DIRIME/          o bien
/media/Personal/PLANERAI/DIRIME/
```
Si algún path falla: verificar que el symlink ~/DIRIME apunte
a /media/Personal/PLANERAI/DIRIME/

### Reglas operativas:
- "Sin descargas" en un prompt = el archivo se crea en el repo, no se descarga
- "Anclas RAG × 4" = incluir 4 sentencias LACHO válidas al final del archivo
- "Formato X.txt" = copiar header exacto del archivo referenciado
- Windsurf puede abrir el repo directamente: cd ~/DIRIME

## ARCHIVOS EN ESTE DIRECTORIO

### Prompts diarios/semanales (ejecutar en orden):
```
$thu 12-03  ← primera semana NOTARIA · base
$fri 13-03  ← NOTARIA KALIL · HTML · endpoints
$sat 14-03  ← BACKUP · BALLPAPER · github_sync · IA ← HOY
$sun 15-03  ← próximo
$mon 16-03  ← próximo
$tue 17-03  ← próximo
$wed 18-03  ← próximo
$thu 19-03 to $wed 25-03 ← semana 2 METHOD × 4 NEURONAS
$thu 26-03 to $wed 01-04 ← semana 3
$thu 02-04 to $wed 08-04 ← semana 4 SECURITY RUNNER
```

### Documentación adicional:
```
PLAN MENSUAL DIRIME IMV · $wed 08-04 → $fri 08-05.txt  ← plan activo
PLAN MENSUAL · $fri 08-05 → $mon 08-06.txt              ← plan siguiente
INFORME_COHERENCIA_PLAN_MENSUAL.txt                      ← verificado ✅
TAREAS_NO_PROCESABLES_DOCUMENTACION.txt                  ← tareas manuales
cloud_agent_notaria_extension.txt                        ← extensión cloud_agent
```

## CARPETAS ESPEJO (subdirectorios)

Este directorio contiene copias de partes del repo para
contexto offline durante optimización de prompts:
```
CORPUS/                   ← espejo parcial de ~/DIRIME/CORPUS/
ELPULSAR LOCAL/           ← espejo de FOLDERS NO RAG INPUT/ELPULSAR LOCAL/
FOLDERS NO RAG INPUT/     ← espejo parcial
```
⚠️ Las copias espejo pueden estar desactualizadas.
   Siempre usar los originales en ~/DIRIME/ para ejecutar.

## ESTADO DE IMPLEMENTACIÓN DE PROMPTS

Cada prompt tiene uno de estos estados:
```
✅ EJECUTADO  → el archivo existe en el repo · verificado
⚠️ PARCIAL   → ejecutado pero incompleto · revisar
❌ PENDIENTE  → no ejecutado aún
🔒 BLOQUEADO  → requiere prerequisito no disponible
```

## CONEXIÓN CON ASKINGS

Los prompts de este directorio son la salida humanamente
editada de los asks generados en:
  Askings for autoresearching by technical horizons/

Flujo ideal (cuando autoresearch_gap.py esté implementado):
```
autoresearch_gap.py → $dia_asks_DDMM.txt
                              ↓
              operador revisa y expande
                              ↓
$dia DD-MM prompts a optimizar para Windsurf.txt
                              ↓
                        Windsurf ejecuta
```

## VARIABLES DE CONTEXTO (siempre vigentes)

Copiar al inicio de cada sesión con Windsurf:
```
Repo: ~/DIRIME (symlink → /media/Personal/PLANERAI/DIRIME/)
Branch: main
Stack: Windsurf + Groq llama-3.3-70b (key en IMV/config/api.json)
Estado: TX=1335 · cristales=42 · S=0.78 · tests=44/44
Python: python3 ~/DIRIME/IMV/main.py
Tests:  cd ~/DIRIME/IMV && python3 -m pytest tests/ -v
Commit: bash ~/DIRIME/tools/github_sync.sh
```

[term] :: activo · [seal of secrecy] :: activo · 空聽數