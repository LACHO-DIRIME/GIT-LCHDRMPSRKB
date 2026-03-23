# UPGRADE_TASKING
# DIRIME/IMV · Upgrade Tasks & Planning
#
# SECUENCIA: [PASO 4 de 4]
#   ← PASO 3: JOURNAL/PLAN_IMPLEMENTACION_BLOQUE_B.md
#   → abrir el archivo $dia DD-MM del día actual · ejecutar en Windsurf
#
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

## 📋 ESTRUCTURA DEL DIRECTORIO

### 📋 ORGANIZACIÓN POR CARPETAS
```
01_TAREAS_INMEDIATAS/     ← Prioridad ALTA - V0.3.0 finalización
02_TAREAS_DESARROLLO/     ← Prioridad MEDIA - Mejoras adicionales
03_TAREAS_PLANIFICACION/  ← Prioridad BAJA - V0.4.0 y futuro
04_PLANES_HISTORICOS/     ← Planes mensuales completados
05_DOCUMENTACION/         ← Documentación de soporte
06_BACKUP_Y_SEGURIDAD/    ← Backups y seguridad
07_REGISTROS_MANTENIMIENTO/ ← Historial de cambios
```

### 📋 CONTENIDO POR CATEGORÍA

#### 📋 01_TAREAS_INMEDIATAS
```bash
📋 TAREAS_PROXIMAS.md ← Plan de trabajo V0.3.0
📋 TAREA 1: CORPUS expansion (+7 docs) 🔥
📋 TAREA 2: Scalar S optimization (0.822 → 0.88) 🔥
📋 TAREA 3: V0.3.0 final validation 🔥
```

#### 📋 02_TAREAS_DESARROLLO
```bash
📋 README.md ← Guía de desarrollo
📋 TAREA 4: cloud_agent_notaria implementation 📋
📋 TAREA 5: GUI V0.3.0 enhancements 📋
📋 TAREA 6: spool_tx optimization 📋
```

#### 📋 03_TAREAS_PLANIFICACION
```bash
📋 README.md ← Guía de planificación
📋 TAREA 7: V0.4.0 roadmap definition 📋
📋 TAREA 8: Production deployment 📋
📋 TAREA 9: Documentation final V0.3.0 📋
```

#### 📋 04_PLANES_HISTORICOS
```bash
📋 README.md ← Guía histórica
📋 PLAN_MENSUAL_COMPLETADO_08-04-08-05.txt ← Semana 4
📋 PLAN_MENSUAL_COMPLETADO_08-05-08-06.txt ← Mes siguiente
📋 PLANES_MENSUALES_ARCHIVADOS_2026-05-18.txt ← Registro
```

#### 📋 05_DOCUMENTACION
```bash
📋 README.md ← Guía de documentación
📋 INFORME_COHERENCIA_PLAN_MENSUAL.txt ← Validación
📋 TAREAS_NO_PROCESABLES_DOCUMENTACION.txt ← Procedimientos
```

#### 📋 06_BACKUP_Y_SEGURIDAD
```bash
📋 README.md ← Guía de seguridad
📋 backup_2026-05-18_optimization_prompts.tar.gz ← Backup completo
```

#### 📋 07_REGISTROS_MANTENIMIENTO
```bash
📋 README.md ← Guía de mantenimiento
📋 LIMPIEZA_COMPLETADA_2026-05-18.txt ← Limpieza
📋 RENOMBRADO_2026-05-18.txt ← Renombrado
📋 PLANES_MENSUALES_ARCHIVADOS_2026-05-18.txt ← Archivado
📋 MOVIMIENTO_ARCHIVOS_2026-05-18.txt ← Movimiento
📋 ESTADO_FINAL_2026-05-18.txt ← Estado final
```

## ESTADO DE IMPLEMENTACIÓN DE UPGRADES

Cada upgrade tiene uno de estos estados:
```
✅ COMPLETADO  → el upgrade está implementado y verificado
⚠️ PARCIAL     → implementado pero incompleto · revisar
❌ PENDIENTE   → no implementado aún
🔒 BLOQUEADO   → requiere prerequisito no disponible
```

## CONEXIÓN CON ASKINGS

Los upgrades de este directorio son la salida humanamente
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
Estado: TX=2026 · cristales=60 · S=0.8 · tests=44/44
Python: python3 ~/DIRIME/IMV/main.py
Tests:  cd ~/DIRIME/IMV && python3 -m pytest tests/ -v
Commit: bash ~/DIRIME/tools/github_sync.sh
```

## HISTORIAL DE UPGRADES

### Completados:
- **Semana 1**: Security RUNNER expansion ✅
- **Semana 2**: KALIL agents + grammar patch ✅
- **Semana 3**: DIRIME V3 CAPA C skeleton ✅
- **Semana 4**: GUI SPOOL V0.3.0 GATE ✅
- **Mes siguiente**: [LOGISTICAL-EXECUTIVE] × PAPER FRONTEND ✅

### En progreso:
- **V0.3.0 Finalization**: 80% completado
- **Tareas próximas**: Estructuradas y priorizadas
- **V0.4.0 Planning**: Pendiente de inicio

## BACKUP Y RECUPERACIÓN

Backup completo disponible:
```
backup_2026-05-18_optimization_prompts.tar.gz
```

Para restaurar si es necesario:
```bash
cd ~/DIRIME/UPGRADE_TASKING
tar -xzf backup_2026-05-18_optimization_prompts.tar.gz
```

[term] :: activo · [seal of secrecy] :: activo · 空聽數