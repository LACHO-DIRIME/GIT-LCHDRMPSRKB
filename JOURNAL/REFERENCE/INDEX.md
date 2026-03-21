# 📚 REFERENCE - Documentación Técnica y Referencias
## [term] :: activo · [seal of secrecy] :: activo · 空聽數

---

## 🎯 **DIRECTORIO REFERENCE**

Contiene toda la documentación técnica, configuración de sistemas y referencias permanentes del proyecto DIRIME/IMV.

---

## 📋 **DOCUMENTACIÓN TÉCNICA**

### 🔧 **INTEGRACIÓN CON IA**

#### **📄 AI_INTEGRATION.md**
```bash
🎯 Propósito: Configuración y uso de IA (Groq, autoresearch)
📊 Contenido: Bridges, prompts, modos de uso, limitaciones
⏱️ Lectura: 8 minutos
🔄 Actualización: Mensual (o al cambiar modelos/bridges)
```

#### **📋 SECCIONES PRINCIPALES**
```bash
🔧 Infraestructura disponible (bridge.py, poke_peek.py)
📋 4 modos de uso (NL→LACHO, autoresearch, structure analyst, CHCL)
🎯 System prompts soberanos
⚠️ Límites honestos y soluciones
```

### 📅 **CALENDARIO SOBERANO**

#### **📄 ALMANAQUE_SOBERANO.md**
```bash
🎯 Propósito: Calendario soberano y ciclos temporales
📊 Contenido: Hexagramas, ciclos MU→KU→WU, fechas importantes
⏱️ Lectura: 5 minutos
🔄 Actualización: Anual (o al agregar eventos importantes)
```

#### **📋 ELEMENTOS DEL CALENDARIO**
```bash
📅 Ciclos diarios MU→KU→WU
🎯 Hexagramas asociados a períodos
📊 Eventos soberanos y hitos
🔄 Sincronización con desarrollo
```

### 📊 **REGISTRO PERMANENTE**

#### **📄 LOG_PERMANENTE.md**
```bash
🎯 Propósito: Registro histórico de eventos importantes
📊 Contenido: Logros, cambios críticos, decisiones soberanas
⏱️ Lectura: 3 minutos (por entrada)
🔄 Actualización: Continua (al ocurrir eventos importantes)
```

#### **📋 TIPO DE ENTRADAS**
```bash
🎉 Hitos alcanzados
🔧 Cambios arquitectónicos
📊 Actualizaciones de métricas
⚠️ Problemas resueltos
🔄 Decisiones estratégicas
```

---

## 🔧 **CONFIGURACIÓN DE SISTEMAS**

### 📋 **BRIDGES Y CONEXIONES**

#### **🔧 Groq Bridge**
```bash
📋 Archivo: DIRIME_v2/groq/bridge.py
🎯 Función: Traducción NL→LACHO, autoresearch
📊 Modelo: llama-3.3-70b-versatile
⚠️ Rate limits: Considerar para uso intensivo
```

#### **🔧 POKE/PEEK System**
```bash
📋 Archivo: DIRIME_v2/fabric/poke_peek.py
🎯 Función: Memoria persistente entre sesiones
📊 Base: sovereign.db
🔄 Uso: Mantener contexto de autoresearch
```

#### **🔧 Ollama Bridge (futuro)**
```bash
📋 Archivo: DIRIME_v3/ollama_bridge/
🎯 Función: Swap transparente Groq→Ollama
📊 Trigger: Hardware Ryzen disponible
⏳ Estado: Esqueleto preparado
```

---

### 📋 **SISTEMAS DE AUTOMATIZACIÓN**

#### **🤖 Autoresearch**
```bash
📋 Archivo: tools/autoresearch_specs.py
🎯 Función: Scanner filesystem + sovereign.db
📊 Output: JSON + YAML estructurado
🔄 Uso: Detección de gaps técnicos
```

#### **🤖 Gap Detection**
```bash
📋 Archivo: tools/autoresearch_gap.py
🎯 Función: Gap detector + Groq bridge
📊 Output: $dia_asks_DDMM.txt
🔄 Uso: Generación automática de tareas
```

---

## 📚 **REFERENCIAS DE DESARROLLO**

### 🎯 **ARQUITECTURA**

#### **📋 Componentes Core**
```bash
🔧 grammar.py → Validador de sentencias LACHO
📊 ledger.py → HL Fabric ledger
🤖 rag.py → BM25 + Behavioral RAG
🧠 samu.py → Sistema SAMU
📋 taxonomy.py → Clasificación soberana
```

#### **📋 Sistemas Derivados**
```bash
🔧 foundation.py → Condiciones soberanas
📊 language_routing.py → NL→LACHO routing
🧠 ceo_alpha.py → CEO Alpha thresholds
📋 chat.py → Interfaz de chat
🔧 main.py → Entry point principal
```

### 🎯 **MÉTRICAS Y MONITOREO**

#### **📊 Scalar S**
```bash
📈 Fórmula: valid/total × (1-unresolved/10)
🎯 Target: ≥0.90 (óptimo), ≥0.70 (operativo)
📋 Estado actual: 0.8 (operativo)
🔄 Cálculo: En cada validación de sentencia
```

#### **📊 LACHO Score**
```bash
📈 Rango: 0.0 → 1.0
🎯 Componentes: Verbo canónico + sujeto + nudo + warnings
📋 Estado actual: 0.8
🔄 Uso: Calidad de sentencias LACHO
```

---

## 🔍 **SISTEMAS DE BÚSQUEDA**

### 📋 **RAG - Retrieval Augmented Generation**

#### **🔍 Cognitive RAG**
```bash
📊 Fuente: CORPUS/ (259+ documentos)
🎯 Función: Recuperación semántica
📋 Boost: Askings/ × 1.5
🔄 Motor: BM25
```

#### **🔍 Behavioral RAG**
```bash
📊 Fuente: ledger soberano
🎯 Función: Patrones de conducta
📋 Contexto: Decisiones pasadas
🔄 Motor: SQLite + HL Fabric
```

---

## 🎯 **REFERENCIAS CRUZADAS**

### 📁 **CONEXIONES INTERNAS**

#### **📋 ACTIVE/**
```bash
📄 SESION_ACTIVA.md → Estado actual del sistema
📄 PENDIENTES.md → Técnicas requeridas
📄 ARCHITECTURE.md → Estado de componentes
```

#### **📋 PLANNING/**
```bash
📄 PLAN_IMPLEMENTACION_BLOQUE_B.md → Técnicas del sprint
📄 PLAN_SEMANAS.md → Objetivos técnicos
📄 PLAN-LACHO-SEMANAS.md → Roadmap técnico LACHO
```

#### **📄 TEMPLATES/**
```bash
📄 INICIO_SESION.md → Contexto técnico para IA
```

---

## 🔧 **HERRAMIENTAS Y UTILIDADES**

### 📋 **COMANDOS ÚTILES**

#### **🔧 Estadísticas del Sistema**
```bash
cd ~/DIRIME/IMV && python3 main.py --stats
📊 Output: TX, cristales, Scalar S, tests, etc.
```

#### **🔧 Validación de Sentencias**
```bash
cd ~/DIRIME/IMV && python3 main.py --validate "{sentencia}"
📊 Output: Resultado de validación LACHO
```

#### **🔧 Autoresearch**
```bash
cd ~/DIRIME/IMV && python3 main.py --asks
📊 Output: Generación automática de tareas
```

#### **🔧 Tests**
```bash
cd ~/DIRIME/IMV && python3 -m pytest tests/ -v
📊 Output: Resultados de pruebas unitarias
```

---

### 📋 **CONFIGURACIÓN**

#### **🔧 API Keys**
```bash
📋 Archivo: IMV/config/api.json
🎯 Contenido: Groq API key, configuración
🔄 Actualización: Manual (al cambiar keys)
```

#### **🔧 Foundation**
```bash
📋 Archivo: IMV/config/foundation.json
🎯 Contenido: Estado foundation, identidad, corpus
🔄 Actualización: Automática (verificación)
```

---

## 🎨 **ESTÁNDARES DE DOCUMENTACIÓN**

### 📋 **FORMATO TÉCNICO**

#### **✅ ESTRUCTURA ESTÁNDAR**
```markdown
# NOMBRE_ARCHIVO.md — Descripción técnica
# [term] :: activo · [seal of secrecy] :: activo · 空聽數

## 🔧 PROPÓSITO
## 📋 IMPLEMENTACIÓN
## 🎯 EJEMPLOS DE USO
## ⚠️ LIMITACIONES
## 🔧 MANTENIMIENTO
```

#### **✅ ELEMENTOS REQUERIDOS**
```markdown
📋 Referencias a archivos de código
🔧 Comandos de ejemplo
⚠️ Casos límite y errores
🔄 Procedimientos de actualización
📊 Métricas de rendimiento
```

---

## 🔄 **MANTENIMIENTO DE REFERENCIAS**

### 📋 **ACTUALIZACIONES PROGRAMADAS**

#### **📅 FRECUENCIAS**
```bash
📅 Semanal: Revisar logs y actualizar documentación
📅 Mensual: Verificar bridges y configuración
📅 Trimestral: Actualizar arquitectura y métricas
📅 Anual: Revisar calendario soberano
```

#### **📋 CRITERIOS DE ACTUALIZACIÓN**
```bash
✅ Cambio en arquitectura del sistema
✅ Nueva herramienta o bridge agregado
✅ Cambio significativo en métricas
✅ Actualización de modelos de IA
```

---

## 🎯 **PRÓXIMOS PASOS**

### 📋 **MEJORAS DE DOCUMENTACIÓN**
```bash
[ ] Agregar diagramas de arquitectura
[ ] Crear glosario de términos técnicos
[ ] Implementar búsqueda en documentación
[ ] Agregar ejemplos de código
```

### 📋 **AUTOMATIZACIÓN**
```bash
[ ] Generación automática de documentación
[ ] Sincronización con código fuente
[ ] Alertas de documentación desactualizada
[ ] Integración con sistema de versionado
```

---

## 🎉 **CONCLUSIÓN**

### ✅ **SISTEMA DE REFERENCIA COMPLETO**

**El directorio REFERENCE está organizado para:**

1. **📚 Documentación técnica completa y accesible**
2. **🔧 Configuración de sistemas clara y mantenible**
3. **📊 Referencias cruzadas con otros componentes**
4. **🔄 Actualizaciones programadas y mantenimiento**

**La documentación técnica está lista para soportar el desarrollo efectivo del proyecto DIRIME.**

---

## 📞 **SOPORTE**

**Para asistencia técnica:**
- 📋 Consultar `../README.md` → Guía general del JOURNAL
- 📋 Revisar `ACTIVE/ARCHITECTURE.md` → Estado actual
- 📋 Ver `PLANNING/PLAN_IMPLEMENTACION_BLOQUE_B.md` → Contexto técnico

**🚀 ¡Directorio REFERENCE listo para consulta técnica! 🚀**
