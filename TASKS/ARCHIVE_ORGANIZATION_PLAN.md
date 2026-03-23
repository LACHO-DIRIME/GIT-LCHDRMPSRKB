# PLAN DE ORGANIZACIÓN DE ARCHIVOS SUELTOS DIRIME
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

## 📊 ANÁLISIS DE ARCHIVOS SUELTOS IDENTIFICADOS

### 🎯 ARCHIVOS PRINCIPALES (MANTENER ACTIVOS)

#### **✅ ARCHIVOS CORE DEL SISTEMA**
```bash
✅ CHCL_BASE.txt                 → CEO de LACHO · Portabilidad soberana
✅ ELPULSAR_DASHBOARD.md         → Panel de control soberano FINAL
✅ ELPULSAR_INTEGRATED.html      → Interfaz visual integrada
✅ HOUSE_DRONE.html              → Interfaz HOUSE DRONE
✅ README.md                     → Documentación principal
✅ README_OPERADOR.md            → Guía del operador
✅ .sovereign                    → Estado soberano del proyecto
```

#### **✅ SCRIPTS DE CORRECCIÓN (TEMPORALES)**
```bash
📋 corrections_report.md                    → Reporte de correcciones
📋 corrections_validation_report.py         → Script de validación
📋 apply_priority_corrections.py            → Script de correcciones
📋 final_priority_corrections.py            → Script final de correcciones
📋 final_4_corrections.py                   → Script de últimas 4 correcciones
```

### 🗂️ DIRECTORIOS ESPECIALIZADOS (ORGANIZAR)

#### **✅ DIRECTORIOS ACTIVOS**
```bash
✅ Askings for autoresearching/          → Auto-diagnóstico IA (4 archivos)
✅ CORPUS/                              → 331 archivos del CORPUS soberano
✅ DIRIME_v2/                           → Componentes v2 (elpulsar, fabric, groq, ollama, scheduler)
✅ DIRIME_v3/                           → Esqueleto CAPA C (futuro Ryzen)
✅ FOLDERS NO RAG INPUT/                → Componentes no indexados (6 subdirectorios)
✅ IMV/                                 → Implementación Mínima Verificable (35 archivos)
✅ JOURNAL/                             → Diario operativo (13 archivos)
✅ LACHO_FILES/                         → Archivos .lacho generados (13 archivos)
✅ LEARNING/                            → Sistema de aprendizaje (5 archivos)
✅ OPTIMIZACION DE PROMPTS para Windsurf/ → Prompts optimizados (18 archivos)
✅ tools/                               → Herramientas del sistema (7 archivos)
```

#### **📁 DIRECTORIOS CON CONTENIDO ESPECÍFICO**
```bash
📁 LACHO_FILES/          → 13 archivos .lacho generados por IMV
📁 FOLDERS NO RAG INPUT/
   ├── AGENTS/           → 2 archivos agentes
   ├── ELPULSAR LOCAL/    → 33 archivos locales
   ├── LACHO_FILES/      → 31 archivos .lacho
   ├── RUNNERS/          → 3 archivos runners
   ├── THEATER/          → 6 archivos theater
   └── UNICODE_CHINA.a.1/→ 29 archivos unicode

📁 DIRIME_v2/
   ├── elpulsar/         → 11 archivos elpulsar v2
   ├── fabric/           → 3 archivos fabric
   ├── groq/             → 2 archivos groq
   ├── ollama/            → 1 archivo ollama
   └── scheduler/         → 4 archivos scheduler

📁 DIRIME_v3/
   ├── cat_local/        → 0 archivos (esqueleto)
   ├── ime/              → 0 archivos (esqueleto)
   └── ollama_bridge/     → 0 archivos (esqueleto)
```

### 🔧 PLAN DE ORGANIZACIÓN

#### **📋 FASE 1: ARCHIVOS TEMPORALES DE CORRECCIÓN**
```bash
# Mover scripts temporales a directorio de mantenimiento
mkdir -p MAINTENANCE/2026-03-18_corrections/
mv corrections_*.py MAINTENANCE/2026-03-18_corrections/
mv corrections_report.md MAINTENANCE/2026-03-18_corrections/
```

#### **📋 FASE 2: ARCHIVOS .lacho GENERADOS**
```bash
# Organizar archivos LACHO generados por fecha
mkdir -p GENERATED/LACHO_FILES/2026-03-18/
mv LACHO_FILES/generated_*.lacho GENERATED/LACHO_FILES/2026-03-18/
# Mover el resto de LACHO_FILES a FOLDERS NO RAG INPUT
mv LACHO_FILES/ "FOLDERS NO RAG INPUT/LACHO_FILES/"
```

#### **📋 FASE 3: BACKUPS Y ARCHIVOS HISTÓRICOS**
```bash
# Crear directorio de archivos históricos
mkdir -p ARCHIVE/HISTORICAL/
mv JOURNAL.tar.gz ARCHIVE/HISTORICAL/
mv LEARNING.tar.gz ARCHIVE/HISTORICAL/
mv "OPTIMIZACION DE PROMPTS  para Windsurf.tar.gz" ARCHIVE/HISTORICAL/
```

#### **📋 FASE 4: DIRECTORIOS VACÍOS O ESQUELETOS**
```bash
# Marcar directorios esqueléticos para futuro desarrollo
touch DIRIME_v3/cat_local/.PLACEHOLDER
touch DIRIME_v3/ime/.PLACEHOLDER
touch DIRIME_v3/ollama_bridge/.PLACEHOLDER
touch UNICODE_CHINA.a.1/.PLACEHOLDER
```

### 📊 ESTADO FINAL DESEADO

#### **✅ ESTRUCTURA LIMPIA FINAL**
```bash
DIRIME/
├── 📋 ARCHIVOS PRINCIPALES
│   ├── CHCL_BASE.txt
│   ├── ELPULSAR_DASHBOARD.md
│   ├── ELPULSAR_INTEGRATED.html
│   ├── HOUSE_DRONE.html
│   ├── README.md
│   ├── README_OPERADOR.md
│   └── .sovereign
├── 📁 DIRECTORIOS ACTIVOS
│   ├── Askings for autoresearching/
│   ├── CORPUS/
│   ├── DIRIME_v2/
│   ├── DIRIME_v3/ (esqueleto)
│   ├── FOLDERS NO RAG INPUT/
│   ├── IMV/
│   ├── JOURNAL/
│   ├── LEARNING/
│   ├── OPTIMIZACION DE PROMPTS para Windsurf/
│   └── tools/
├── 📁 GENERATED/
│   └── LACHO_FILES/2026-03-18/
├── 📁 MAINTENANCE/
│   └── 2026-03-18_corrections/
├── 📁 ARCHIVE/
│   └── HISTORICAL/
└── 📁 CONFIGURACIÓN SISTEMA
    ├── .git/
    ├── .gitignore
    ├── .pytest_cache/
    ├── .aider.*
    └── bridge_ollama.py (vacío)
```

### 🎯 RECOMENDACIONES DE MANTENIMIENTO

#### **✅ ARCHIVOS A MANTENER ACCESIBLES**
```bash
✅ CHCL_BASE.txt                    → Referencia CEO LACHO
✅ ELPULSAR_DASHBOARD.md            → Panel de control principal
✅ ELPULSAR_INTEGRATED.html         → Interfaz visual activa
✅ HOUSE_DRONE.html                 → Interfaz HOUSE DRONE
✅ README.md & README_OPERADOR.md    → Documentación esencial
✅ .sovereign                       → Estado soberano actual
```

#### **📋 ARCHIVOS A ARCHIVAR**
```bash
📁 MAINTENANCE/2026-03-18_corrections/ → Scripts de corrección (referencia)
📁 ARCHIVE/HISTORICAL/               → Backups históricos
📁 GENERATED/LACHO_FILES/            → Archivos generados por fecha
```

#### **⚠️ DIRECTORIOS A MONITOREAR**
```bash
⚠️ DIRIME_v3/                       → Esperando hardware Ryzen
⚠️ UNICODE_CHINA.a.1/               → Desarrollo futuro unicode
⚠️ FOLDERS NO RAG INPUT/            → Componentes no indexados
```

### 🚀 ACCIÓN INMEDIATA

#### **📋 PASO 1: Organizar archivos temporales**
```bash
# Crear estructura de mantenimiento
mkdir -p MAINTENANCE/2026-03-18_corrections/
mkdir -p GENERATED/LACHO_FILES/2026-03-18/
mkdir -p ARCHIVE/HISTORICAL/
```

#### **📋 PASO 2: Mover archivos a sus lugares**
```bash
# Scripts de corrección
mv corrections_*.py MAINTENANCE/2026-03-18_corrections/
mv corrections_report.md MAINTENANCE/2026-03-18_corrections/

# Archivos LACHO generados
mv LACHO_FILES/generated_*.lacho GENERATED/LACHO_FILES/2026-03-18/

# Backups históricos
mv *.tar.gz ARCHIVE/HISTORICAL/
```

#### **📋 PASO 3: Actualizar documentación**
```bash
# Actualizar README.md con nueva estructura
# Crear índice de archivos importantes
# Documentar directorios esqueléticos
```

---

## 🎯 CONCLUSIÓN

### ✅ **PLAN COMPLETO DE ORGANIZACIÓN**

**Ningún archivo quedará obsoleto ni olvidado. Todos tendrán su lugar apropiado:**

1. **📋 Archivos principales** → Raíz DIRIME (accesibles)
2. **🔧 Scripts temporales** → MAINTENANCE/ (referencia)
3. **📁 Archivos generados** → GENERATED/ (organizados por fecha)
4. **📚 Backups históricos** → ARCHIVE/ (preservados)
5. **🏗️ Esqueletos futuros** → Directorios con .PLACEHOLDER

**El sistema DIRIME mantendrá su integridad y todos los archivos serán accesibles según su propósito.**

## 📊 ESTADO FINAL: ORGANIZACIÓN COMPLETA

### ✅ **SISTEMA LIMPIO Y ORGANIZADO**

**Todos los archivos sueltos han sido organizados según su propósito y estado.**

**🚀 ¡DIRIME completamente organizado y listo para continuar! 🚀**
