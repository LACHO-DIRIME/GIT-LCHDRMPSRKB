# DIRIME — Plataforma Operativa Soberana

## 📖 Qué es DIRIME

DIRIME es la plataforma operativa soberana completa. IMV es su implementación mínima verificable.

- **DIRIME**: Dos nodos físicos, HL FABRIC real, WEB3, Scheduler OS, corpus completo.
- **IMV**: Subconjunto mínimo que demuestra que LACHO funciona como código ejecutable soberanamente.

## 🏗️ Arquitectura

```
DIRIME/
├── CORPUS/           # Subconjunto operativo del LIBRO (36 archivos)
├── IMV/              # Implementación Mínima Verificable
│   ├── config/       # Externalización soberana
│   ├── core/         # Módulos principales
│   ├── interface/    # Chat AI (4 niveles de traducción)
│   ├── data/         # SQLite HL FABRIC provisional
│   ├── logs/         # Logs soberanos (futuro)
│   └── tests/        # Tests soberanos (futuro)
└── .sovereign        # Estado soberano del proyecto
```

## 🚀 Instalación

### Requisitos base (siempre necesarios)
```bash
python>=3.10
rich>=13.0.0
pydantic>=2.0.0
```

### Nivel 0: Gramática directa (recomendado para uso operativo)
```bash
git clone <repo>
cd DIRIME
pip install -r IMV/requirements.txt  # Solo dependencias base
python main.py
DIRIME> TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]
```

### Nivel 1: 20 patrones hardcodeados (activo por defecto)
```bash
# Mismo que Nivel 0, pero puedes escribir:
DIRIME> verificar el sistema
DIRIME> custodiar activo soberano
DIRIME> dirimir disputa activa
```

### Nivel 2: API externa (opcional)
```bash
# 1. Descomentar openai>=1.0.0 en requirements.txt
# 2. pip install openai
# 3. cp IMV/config/api.json.example IMV/config/api.json
# 4. Editar api.json con tu clave real
# 5. python main.py
DIRIME> quiero verificar que el sistema esté operativo
# → Traducción real vía API externa
```

### Nivel 3: Modelo local Ollama (futuro)
```bash
# 1. Instalar Ollama: curl -fsSL https://ollama.ai/install.sh | sh
# 2. ollama pull deepseek-coder:6.7b
# 3. cp IMV/config/ollama.json.example IMV/config/ollama.json
# 4. python main.py
DIRIME> necesito auditar la coherencia del sistema
# → Traducción local sin internet
```

## 💡 Uso

### Modo interactivo (default)
```bash
python main.py
DIRIME> [tu comando LACHO o lenguaje natural]
```

### Validación directa
```bash
python main.py --validate "TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]"
```

### Estadísticas del sistema
```bash
python main.py --stats
# → Transacciones, cristales, precisión, Scalar S
```

### Ayuda
```bash
python main.py --help
DIRIME> help
DIRIME> ?
```

## 📚 Corpus Soberano

### LIBRO (fuente de verdad)
- **Ubicación**: `/RESULTADO DE ANALISIS/ACOPIADO/LIBRO/`
- **Contenido**: 175 archivos constitucionales
- **Propósito**: Especificación completa del sistema

### CORPUS (subconjunto operativo)
- **Ubicación**: `./CORPUS/`
- **Contenido**: 36 archivos referenciados por el código
- **Propósito**: Lo que IMV ejecuta HOY
- **Sincronización**: Siempre desde LIBRO → CORPUS

## 🔧 Configuración Soberana

### foundation.json
```json
{
  "status": "OK",
  "identity_verified": true,
  "corpus_accessible": true,
  "ledger_available": true,
  "notes": []
}
```

### scope.json
```json
{
  "name": "IMV_core_modules",
  "allowed_modules": ["grammar", "samu", "ledger", "chat", "main"],
  "status": "ACTIVE"
}
```

### term.json
```json
{
  "label": "open",
  "status": "OPEN",
  "cycle_id": null
}
```

## 🔄 Ciclo Soberano

1. **Input** → chat.py (traductor de 4 niveles)
2. **Validación** → grammar.py (5 reglas + paradigmas)
3. **Dirimencia** → samu.py (auditor soberano)
4. **Registro** → ledger.py (HL FABRIC SQLite)
5. **Output** → resultado soberano verificable

## 📊 Métricas Soberanas

### Scalar S
- **Rango**: [0,1] coherencia soberana
- **Cálculo**: S = valid_ratio × (1 - red_regret_weight)
- **Umbral operativo**: S ≥ 0.7

### Behavioral RAG
- **Mínimo**: suggest_from_history() basado en frecuencia ≥5
- **Completo**: embeddings + base de vectores (futuro)

### Cristales STACKING
- **Auto-cristalización**: verbos VALID con frecuencia ≥10
- **Pilares**: H01, H02, H04, H23, H29, H30, H48, H51, H52, H57, H58

## 🛡️ Seguridad

- **Claves API**: Nunca commitear api.json/ollama.json
- **Solo .example**: Versionar solo plantillas
- **.gitignore**: Excluir archivos con claves reales

## 🤝 Contribución

### Sincronización CORPUS
```bash
# Cuando actualizas un archivo en LIBRO:
cp "/LIBRO/BIBLIO-SOURCES(NUEVO).txt" "./CORPUS/"
# Actualizar CORPUS_INDEX.md
# Actualizar INDICE_MAESTRO_ACTUALIZABLE.txt
```

### Agregar nuevo módulo
1. Implementar módulo en IMV/core/
2. Crear BIBLIO-SOURCES en LIBRO/
3. Copiar a CORPUS/
4. Actualizar documentación
5. Probar ciclo soberano completo

## 📄 Referencias

- **CORPUS_INDEX.md**: Mapa completo del corpus operativo
- **.sovereign**: Estado actual del proyecto
- **BIBLIO-SOURCES**: Documentación constitucional completa

## 🎯 Objetivo

DIRIME demuestra que la soberanía es posible: un sistema operativo donde la verdad es local, la autoridad es soberana, y el lenguaje es ejecutable sin intermediarios.

IMV es la prueba verificable de que este principio funciona en código real hoy.

---

**Estado actual**: IMV v0.1.0 — Ciclo soberano operativo en Niveles 0 y 1.  
**Próximo**: v0.2.0 — Scalar S + Behavioral RAG + validación por paradigmas.
