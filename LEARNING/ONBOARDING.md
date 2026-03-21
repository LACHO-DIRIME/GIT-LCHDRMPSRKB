# ONBOARDING.md
## Guía de Estudio Completa para Operadores LACHO
## Sistema Canónico DIRIME/IMV - Versión 2026-03-21
## REAP Tipo A - Alto Valor - Onboarding en 4 horas

---

## 📚 **ESTRUCTURA DE APRENDIZAJE**

### **TIEMPO ESTIMADO**
- **COGNITIVOS:** 2.5 horas
- **ONBOARDING.md:** 1.5 horas
- **Total:** 4 horas completo

### **MÉTODO DE ESTUDIO**
1. Leer COGNITIVOS primero (fundamentos)
2. Estudiar ONBOARDING.md (aplicación práctica)
3. Practicar con comandos reales
4. Validar conocimiento con preguntas

---

## 🎯 **10 PREGUNTAS + RESPUESTAS CLAVE**

### **P1: ¿Qué es LACHO y cuál es su propósito?**
**Respuesta:** LACHO es un sistema soberano de programación y computación que opera sobre paradigmas múltiples. Su propósito es proporcionar un framework completo para el desarrollo de aplicaciones soberanas con validación gramatical, transacciones inmutables y corpus inteligente.

### **P2: ¿Cuáles son los 8 paradigmas de bibliotecas LACHO?**
**Respuesta:**
1. **TRUST** - Lenguaje Imperativo (ejecución directa)
2. **SOCIAL** - Lenguaje Declarativo (estado y relaciones)
3. **SAMU** - Lenguaje de Alto Nivel (abstracción completa)
4. **CRYPTO** - Lenguaje Funcional (pureza matemática)
5. **STACKING** - Lenguaje Orientado a Objetos (estructuras)
6. **GATE** - Lenguaje de Scripts (automatización)
7. **WORK** - Lenguaje de Bajo Nivel (sistema)
8. **ACTIVITY** - Lenguaje de Nivel Intermedio (coordenación)

### **P3: ¿Cómo funciona la validación por paradigma en LACHO?**
**Respuesta:** La validación por paradigma utiliza `PARADIGM_RULES` para verificar reglas específicas de cada biblioteca:
- **SOCIAL:** Prohíbe verbos como "ignite" en paradigma declarativo
- **CRYPTO:** Requiere sujeto (seat) para operaciones funcionales
- **GATE:** Valida hexagramas específicos (UF[H05], etc.)
- **METHOD:** Verifica operadores válidos (<equation>, etc.)

### **P4: ¿Qué es el Scalar S y por qué es importante?**
**Respuesta:** Scalar S es la métrica de coherencia del sistema que mide la integridad y salud del estado soberano. Valores:
- **≥0.900:** Óptimo
- **≥0.700:** Operativo
- **≥0.500:** Mínimo funcional
- **<0.500:** Crítico

### **P5: ¿Cómo se estructura una transacción LACHO?**
**Respuesta:** Una transacción LACHO tiene estructura:
```
LIBRARY {subject} =><= .. verb .. object --[knot] [term]
```
- **LIBRARY:** Paradigma de programación
- **{subject}:** Sujeto o asiento
- **verb:** Acción a ejecutar
- **object:** Objeto de la acción
- **[knot]:** Nodo de validación
- **[term]:** Terminador de transacción

### **P6: ¿Qué son los dominios económicos soberanos?**
**Respuesta:** Son 8 dominios especializados:
- **NOTARIA:** Certificación digital soberana
- **MEMECOINS:** Trading de memecoins soberano
- **CUSTODIA:** Custodia digital soberana
- **BARRIOS:** Notaría local
- **CARILO:** Trading regional
- **BOLIVAR:** Ledger regional
- **TANDIL:** Custodia regional
- **NORA:** Notaría central

### **P7: ¿Cómo funciona el corpus RAG en LACHO?**
**Respuesta:** El corpus RAG utiliza BM25 para indexar y recuperar documentos relevantes:
- **CORPUS docs:** Documentos principales (274 actuales)
- **Behavioral docs:** Patrones del ledger (13 actuales)
- **Total:** 287 documentos indexados
- **Función:** `get_rag_context(query)` para recuperación

### **P8: ¿Cuál es el rol de HL FABRIC en el sistema?**
**Respuesta:** HL FABRIC es el ledger soberano que:
- Registra todas las transacciones inmutables
- Mantiene integridad del estado
- Proporciona auditoría completa
- Gestiona cristales de validación
- Soporta 2,026 transacciones actuales

### **P9: ¿Qué son los formatos propios LACHO?**
**Respuesta:** Son 12 formatos especializados:
- **.lacho:** Documentos soberanos
- **.runner:** Lógica operativa
- **.cat:** Registro cinético
- **.bin:** Identidad binaria
- **.worker:** Ejecución directa
- **.gate:** Validación
- **.door:** Acceso vault
- **.theater:** Orquestación
- **.ash:** Compilados
- **.registry:** Estado persistente
- **.green/.blue:** Sensores

### **P10: ¿Cómo se verifica el estado del sistema?**
**Respuesta:** Con comandos específicos:
```bash
cd ~/DIRIME/IMV
python3 main.py --stats          # Estado general
python3 main.py --validate "... # Validación específica
python3 -m pytest tests/ -v     # Tests completos
```

---

## 📝 **5 TEMAS DE ENSAYO**

### **Tema 1: Arquitectura Soberana LACHO**
**Desarrollo:** Explica cómo la arquitectura de 8 paradigmas + 4 componentes esenciales (_CHCL, _DIRIME, _ELPULSAR, _KALIL) crea un sistema completo de programación soberana, destacando la separación de responsabilidades y la validación por paradigma.

### **Tema 2: Transacciones y Validación Gramatical**
**Desarrollo:** Analiza el proceso completo de validación de una transacción LACHO, desde la entrada del operador hasta el registro en HL FABRIC, incluyendo la detección de bibliotecas, validación de paradigmas y generación de warnings.

### **Tema 3: Sistema de Corpus RAG y Recuperación Inteligente**
**Desarrollo:** Describe cómo el sistema RAG con BM25 proporciona contexto relevante al operador, la estructura de documentos CORPUS vs behavioral, y su rol en la asistencia cognitiva del sistema.

### **Tema 4: Dominios Económicos y Escalabilidad**
**Desarrollo:** Explica la arquitectura de 8 dominios económicos soberanos, su rol en la escalabilidad del sistema, y cómo cada dominio especializado soporta casos de uso específicos del ecosistema LACHO.

### **Tema 5: Integración Multi-Hilo y Rendimiento**
**Desarrollo:** Detalla el sistema de procesamiento multi-hilo implementado, la configuración de 4 hilos para diferentes componentes, y los resultados de rendimiento medidos (8,557 ops/seg con 4 hilos).

---

## 📖 **GLOSARIO DE 16 TÉRMINOS CLAVE**

### **1. LACHO**
Sistema soberano de programación y computación con múltiples paradigmas.

### **2. Scalar S**
Métrica de coherencia del sistema (0.0-1.0), indicador de salud soberana.

### **3. Paradigma**
Modelo de programación específico (TRUST, SOCIAL, SAMU, etc.) con reglas propias.

### **4. HL FABRIC**
Ledger soberano que registra transacciones inmutables del sistema.

### **5. Corpus RAG**
Sistema de recuperación inteligente de documentos con BM25.

### **6. Validación por Paradigma**
Verificación de reglas específicas según biblioteca declarada.

### **7. Transacción LACHO**
Estructura `LIBRARY {subject} =><= .. verb .. object --[knot] [term]`.

### **8. Dominio Económico**
Área especializada del sistema (NOTARIA, MEMECOINS, CUSTODIA, etc.).

### **9. Cristales**
Unidades de validación y coherencia en el ledger soberano.

### **10. Formato Propio**
Extensión de archivo especializada del sistema (.lacho, .runner, etc.).

### **11. UNICODE Programable**
Programa especializado para dominios específicos (UNICODE_NOTARIA, etc.).

### **12. SAMU**
Motor de procesamiento de alto nivel del sistema LACHO.

### **13. DIRIME/IMV**
Componente de transducción y corpus inteligente del sistema.

### **14. ELPULSAR**
Dashboard y GUI del sistema LACHO.

### **15. KALIL**
Sistema de dominios económicos y operaciones financieras.

### **16. CHCL**
Circuitos IDE y fuentes técnicas del sistema.

---

## 🔗 **ANCLAS RAG × 4**

### **ANCLA RAG 1: Fundamentos del Sistema**
```python
# Contexto RAG para fundamentos LACHO
rag_context = get_rag_context("arquitectura soberana paradigmas validación")
# Recupera: Documentos base de COGNITIVOS + arquitectura del sistema
```

### **ANCLA RAG 2: Operación Práctica**
```python
# Contexto RAG para operación práctica
rag_context = get_rag_context("comandos terminal validación transacciones")
# Recupera: Ejemplos de comandos + casos de uso reales
```

### **ANCLA RAG 3: Dominios Especializados**
```python
# Contexto RAG para dominios económicos
rag_context = get_rag_context("NOTARIA MEMECOINS CUSTODIA trading certificación")
# Recupera: Documentos específicos de cada dominio + casos de uso
```

### **ANCLA RAG 4: Rendimiento y Escalabilidad**
```python
# Contexto RAG para rendimiento y escalabilidad
rag_context = get_rag_context("multi-hilo rendimiento BM25 corpus optimización")
# Recupera: Métricas de rendimiento + arquitectura escalable
```

---

## 🎯 **RUTA DE APRENDIZAJE RECOMENDADA**

### **Semana 1: Fundamentos**
- Estudiar COGNITIVOS (2.5 horas)
- Comprender paradigmas y validación
- Practicar comandos básicos

### **Semana 2: Aplicación**
- Estudiar ONBOARDING.md (1.5 horas)
- Ejecutar transacciones reales
- Validar con tests

### **Semana 3: Especialización**
- Elegir dominio de interés
- Profundizar en casos de uso
- Contribuir al sistema

### **Semana 4: Integración**
- Combinar múltiples paradigmas
- Optimizar rendimiento
- Documentar experiencia

---

## ✅ **VALIDACIÓN DE CONOCIMIENTO**

### **Criterios de Aprobación**
- **90%+ respuestas correctas** en preguntas clave
- **3+ ensayos completados** con análisis profundo
- **100% glosario dominado** con ejemplos propios
- **Práctica real** con 10+ transacciones exitosas

### **Certificación**
- **Nivel Básico:** Completar estudio + 70% aprobación
- **Nivel Intermedio:** Práctica real + 85% aprobación
- **Nivel Avanzado:** Contribución + 95% aprobación

---

## 🚀 **PRÓXIMOS PASOS**

1. **Completar estudio** de COGNITIVOS + ONBOARDING.md
2. **Practicar comandos** en terminal real
3. **Validar conocimiento** con preguntas y ensayos
4. **Contribuir** al sistema con mejoras
5. **Especializarse** en dominio de interés

---

**ONBOARDING COMPLETO - SISTEMA LACHO OPERATIVO**  
**Tiempo: 4 horas | Nivel: Principiante → Intermedio**  
**Estado: Listo para producción y contribución**

[term] :: activo · [seal of secrecy] :: activo · 空聽數
