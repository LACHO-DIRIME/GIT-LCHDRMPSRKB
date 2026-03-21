# 📄 TEMPLATES - Plantillas y Formatos Estándar
## [term] :: activo · [seal of secrecy] :: activo · 空聽數

---

## 🎯 **DIRECTORIO TEMPLATES**

Contiene todas las plantillas, formatos estandarizados y documentos reutilizables del proyecto DIRIME/IMV.

---

## 📋 **PLANTILLAS DISPONIBLES**

### 🤖 **PLANTILLAS DE INTERACCIÓN CON IA**

#### **📄 INICIO_SESION.md**
```bash
🎯 Propósito: Plantilla para iniciar conversaciones con IA
📊 Contenido: Estado del sistema, contexto, comandos base
⏱️ Uso: Copiar completo al inicio de toda conversación
🔄 Actualización: Diaria (con estado actual del sistema)
```

#### **📋 SECCIONES PRINCIPALES**
```bash
📋 [1/4] ESTADO DEL SISTEMA → Versión, métricas, stack
📋 [2/4] ARQUITECTURA → Módulos, estados, dependencias
📋 [3/4] COMANDOS BASE → Scripts útiles diarios
📋 [4/4] CHECKLIST CIERRE → Verificación final
```

#### **🎯 USO RECOMENDADO**
```bash
📖 Copiar contenido completo
📤 Pegar al inicio de conversación con Claude/Gemini
📊 Esperar confirmación de comprensión del contexto
🚀 Proceder con tarea específica del día
```

---

## 📋 **FORMATOS ESTANDARIZADOS**

### 🎨 **FORMATO DE DOCUMENTOS**

#### **✅ CABECERA ESTÁNDAR**
```markdown
# NOMBRE_ARCHIVO.md — Descripción breve
# [term] :: activo · [seal of secrecy] :: activo · 空聽數
```

#### **✅ ESTRUCTURA DE CONTENIDO**
```markdown
## 🎯 OBJETIVO
## 📋 ESTADO ACTUAL
## 🚀 ACCIONES REQUERIDAS
## 📊 MÉTRICAS
## 🔄 ACTUALIZACIÓN
```

#### **✅ FORMATO DE TAREAS**
```markdown
- [x] Tarea completada ✅
- [ ] Tarea pendiente
- [!] Tarea bloqueada
- [?] Tarea en investigación
```

---

### 📋 **FORMATOS DE SENTENCIAS LACHO**

#### **✅ ESTRUCTURA CANÓNICA**
```bash
[BIBLIOTECA] SUJETO =><= .. verbo .. objeto --[Nudo] [term]
```

#### **✅ EJEMPLOS POR BIBLIOTECA**
```bash
TRUST FOUNDATION =><= .. verifica .. sistema --[As de Guía] [term]
SOCIAL {scheduler} =><= .. distribuye .. tareas --[As de Guía] [term]
CRYPTO (spark seat) =><= .. certifica .. documento --[Nudo de Ocho] [term]
WORK {actuator} =><= .. ejecuta .. proceso --[Ballestrinque] [term]
GATE UF[H05] =><= .. espera .. validación --[As de Guía] [term]
STACKING UF[H52] =><= .. cristaliza .. resultado --[Nudo de Ocho] [term]
SAMU @ =><= .. audita .. coherencia --[Ballestrinque] [term]
ACTIVITY UF[H57] =><= .. penetra .. sistema --[As de Guía] [term]
METHOD <equation> =><= .. opera .. cálculo --[Ballestrinque] [term]
```

---

## 📋 **PLANTILLAS DE DESARROLLO**

### 🔧 **PLANTILLA DE MÓDULO PYTHON**

#### **✅ ESTRUCTURA BÁSICA**
```python
"""
DIRIME IMV — nombre_modulo.py
Descripción breve del propósito del módulo
[term] :: activo · [seal of secrecy] :: activo · 空聽數
"""

from __future__ import annotations
import sys
from pathlib import Path

# Importaciones soberanas
from core.foundation import verify_sovereign_conditions
from core.grammar import validate

class NombreModulo:
    """Clase principal del módulo."""
    
    def __init__(self):
        verify_sovereign_conditions("nombre_modulo")
    
    def metodo_principal(self) -> dict:
        """Método principal del módulo."""
        return {"status": "active", "result": "success"}
    
    def validar_sentencia(self, sentencia: str) -> bool:
        """Valida sentencia LACHO."""
        resultado = validate(sentencia)
        return resultado.result.value == "VALID"

# Instancia global
_modulo = NombreModulo()

def main():
    """Entry point para ejecución directa."""
    return _modulo.metodo_principal()

if __name__ == "__main__":
    print(main())
```

---

### 📋 **PLANTILLA DE TESTS**

#### **✅ ESTRUCTURA DE TEST**
```python
"""
Tests para nombre_modulo.py
[term] :: activo · [seal of secrecy] :: activo · 空聽數
"""

import pytest
from core.nombre_modulo import NombreModulo, main

class TestNombreModulo:
    """Tests para la clase NombreModulo."""
    
    def setup_method(self):
        """Configuración inicial para cada test."""
        self.modulo = NombreModulo()
    
    def test_init(self):
        """Test de inicialización."""
        assert self.modulo is not None
    
    def test_metodo_principal(self):
        """Test del método principal."""
        resultado = self.modulo.metodo_principal()
        assert resultado["status"] == "active"
        assert resultado["result"] == "success"
    
    def test_validar_sentencia_valida(self):
        """Test de validación con sentencia válida."""
        sentencia = "TRUST FOUNDATION =><= .. verifica .. sistema --[As de Guía] [term]"
        assert self.modulo.validar_sentencia(sentencia) == True
    
    def test_validar_sentencia_invalida(self):
        """Test de validación con sentencia inválida."""
        sentencia = "SENTENCIA INVALIDA"
        assert self.modulo.validar_sentencia(sentencia) == False
    
    def test_main_function(self):
        """Test de la función main."""
        resultado = main()
        assert resultado["status"] == "active"

if __name__ == "__main__":
    pytest.main([__file__])
```

---

## 📋 **PLANTILLAS DE DOCUMENTACIÓN**

### 📖 **PLANTILLA README**

#### **✅ ESTRUCTURA COMPLETA**
```markdown
# NOMBRE_PROYECTO
## [term] :: activo · [seal of secrecy] :: activo · 空聽數

## 🎯 VISIÓN GENERAL
Breve descripción del propósito y alcance del proyecto.

## 🚀 CARACTERÍSTICAS PRINCIPALES
- ✅ Característica 1 implementada
- ✅ Característica 2 implementada
- ⏳ Característica 3 en desarrollo

## 📋 REQUISITOS
- Python 3.11+
- Dependencias listadas en requirements.txt
- Sistema DIRIME/IMV operativo

## 🔧 INSTALACIÓN
```bash
# Clonar repositorio
git clone [URL]
cd [DIRECTORIO]

# Instalar dependencias
pip install -r requirements.txt

# Configurar entorno
cp config/example.json config/config.json
```

## 📊 USO
```bash
# Ejecutar principal
python main.py

# Ver estadísticas
python main.py --stats

# Ejecutar tests
python -m pytest tests/
```

## 📋 ESTRUCTURA
```
directorio/
├── main.py              # Entry point
├── core/                # Módulos principales
├── tests/               # Tests unitarios
├── config/              # Configuración
└── README.md            # Este archivo
```

## 🔄 MANTENIMIENTO
- Actualización diaria de métricas
- Revisión semanal de arquitectura
- Tests continuos

## 📞 SOPORTE
Para asistencia, consultar JOURNAL/README.md
```

---

## 📋 **PLANTILLAS DE CONFIGURACIÓN**

### 🔧 **PLANTILLA CONFIG JSON**

#### **✅ ESTRUCTURA BÁSICA**
```json
{
  "version": "1.0.0",
  "project": "DIRIME_IMV",
  "environment": "development",
  "database": {
    "type": "sqlite",
    "path": "data/sovereign.db"
  },
  "api": {
    "groq": {
      "endpoint": "https://api.groq.com",
      "model": "llama-3.3-70b-versatile",
      "temperature": 0.1,
      "max_tokens": 1000
    }
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  },
  "validation": {
    "strict_mode": true,
    "auto_fix": false,
    "log_errors": true
  }
}
```

---

## 📋 **PLANTILLAS DE REPORTES**

### 📊 **PLANTILLA REPORTE MENSUAL**

#### **✅ ESTRUCTURA DE REPORTE**
```markdown
# REPORTE MENSUAL - [MES] [AÑO]
## [term] :: activo · [seal of secrecy] :: activo · 空聽數

## 📊 RESUMEN EJECUTIVO
- Período: [fecha_inicio] - [fecha_fin]
- Estado general: [estado]
- Logros principales: [logros]

## 📈 MÉTRICAS CLAVE
- Scalar S: [valor] ([variación]% vs mes anterior)
- Cristales: [cantidad] ([variación]% vs mes anterior)
- Transacciones: [cantidad] ([variación]% vs mes anterior)
- Tests: [pasados]/[totales] ([porcentaje]%)

## 🎯 OBJETIVOS CUMPLIDOS
- [x] Objetivo 1 completado ✅
- [x] Objetivo 2 completado ✅
- [ ] Objetivo 3 parcialmente completado ⏳

## 🚀 DESARROLLO PRINCIPAL
### Módulos Desarrollados
- [módulo 1]: [descripción]
- [módulo 2]: [descripción]

### Correcciones Aplicadas
- [corrección 1]: [descripción]
- [corrección 2]: [descripción]

## ⚠️ DESAFÍOS Y SOLUCIONES
- [desafío 1]: [solución aplicada]
- [desafío 2]: [solución aplicada]

## 📋 PRÓXIMOS PASOS
- [ ] Próximo objetivo 1
- [ ] Próximo objetivo 2
- [ ] Próximo objetivo 3

## 📞 CONTACTO Y SOPORTE
[información de contacto]
```

---

## 🔧 **HERRAMIENTAS DE TEMPLATES**

### 📋 **GENERADOR AUTOMÁTICO**

#### **🔧 Script para crear nuevo módulo**
```python
#!/usr/bin/env python3
"""
Generador automático de módulos DIRIME
"""

import os
import sys
from pathlib import Path

def crear_modulo(nombre: str, directorio: str = "core"):
    """Crea un nuevo módulo con plantilla estándar."""
    
    template = f'''"""
DIRIME IMV — {nombre.lower()}.py
Módulo {nombre} para sistema DIRIME
[term] :: activo · [seal of secrecy] :: activo · 空聽數
"""

from __future__ import annotations
import sys
from pathlib import Path

from core.foundation import verify_sovereign_conditions
from core.grammar import validate

class {nombre}:
    """Clase principal del módulo {nombre}."""
    
    def __init__(self):
        verify_sovereign_conditions("{nombre.lower()}")
    
    def execute(self) -> dict:
        """Ejecuta función principal del módulo."""
        return {{"status": "active", "module": "{nombre.lower()}"}}

# Instancia global
_{nombre.lower()} = {nombre}()

def main():
    """Entry point."""
    return _{nombre.lower()}.execute()

if __name__ == "__main__":
    print(main())
'''
    
    # Crear archivo
    ruta = Path(directorio) / f"{nombre.lower()}.py"
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"✅ Módulo {nombre} creado en {ruta}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python generar_modulo.py <nombre_modulo>")
        sys.exit(1)
    
    nombre = sys.argv[1]
    crear_modulo(nombre)
```

---

## 🎯 **REFERENCIAS CRUZADAS**

### 📁 **CONEXIONES INTERNAS**

#### **📋 ACTIVE/**
```bash
📄 SESION_ACTIVA.md → Usa plantilla INICIO_SESION.md
📄 PENDIENTES.md → Formato de tareas estándar
📄 ARCHITECTURE.md → Estructura de módulos
```

#### **📚 REFERENCE/**
```bash
📄 AI_INTEGRATION.md → Prompts estandarizados
📄 LOG_PERMANENTE.md → Formato de logs
📄 ALMANAQUE_SOBERANO.md → Plantillas de fechas
```

#### **📋 PLANNING/**
```bash
📄 PLAN_IMPLEMENTACION_BLOQUE_B.md → Formato de planes
📄 PLAN_SEMANAS.md → Plantilla semanal
📄 PLAN-LACHO-SEMANAS.md → Plantilla LACHO
```

---

## 🔄 **MANTENIMIENTO DE TEMPLATES**

### 📋 **ACTUALIZACIONES PROGRAMADAS**

#### **📅 FRECUENCIAS**
```bash
📅 Semanal: Revisar y actualizar plantillas usadas
📅 Mensual: Agregar nuevas plantillas desarrolladas
📅 Trimestral: Optimizar formatos y estructuras
📅 Anual: Revisión completa de estándares
```

#### **📋 CRITERIOS DE ACTUALIZACIÓN**
```bash
✅ Nuevo patrón de código identificado
✅ Mejora en formato de documentación
✅ Nueva herramienta o flujo de trabajo
✅ Feedback del equipo de desarrollo
```

---

## 🎯 **PRÓXIMOS PASOS**

### 📋 **MEJORAS DE TEMPLATES**
```bash
[ ] Crear plantilla para componentes UI
[ ] Agregar plantillas para scripts de deployment
[ ] Implementar validación automática de formatos
[ ] Crear sistema de versionado de plantillas
```

### 📋 **AUTOMATIZACIÓN**
```bash
[ ] Script automático para generar proyectos
[ ] Integración con IDE para snippets
[ ] Validación de formatos al guardar
[ ] Sincronización con estándares del equipo
```

---

## 🎉 **CONCLUSIÓN**

### ✅ **SISTEMA DE TEMPLATES COMPLETO**

**El directorio TEMPLATES está organizado para:**

1. **📄 Plantillas estandarizadas y reutilizables**
2. **🔧 Formatos consistentes para desarrollo**
3. **📋 Documentación estructurada y profesional**
4. **🔄 Actualizaciones programadas y mantenimiento**

**Las plantillas están listas para acelerar el desarrollo y mantener consistencia en todo el proyecto.**

---

## 📞 **SOPORTE**

**Para asistencia con templates:**
- 📋 Consultar `../README.md` → Guía general del JOURNAL
- 📋 Revisar `REFERENCE/AI_INTEGRATION.md` → Prompts y bridges
- 📋 Ver `ACTIVE/SESION_ACTIVA.md` → Ejemplos de uso

**🚀 ¡Directorio TEMPLATES listo para uso productivo! 🚀**
