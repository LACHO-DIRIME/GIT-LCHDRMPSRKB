# Configuración Soberana — Externalización de Condiciones

## 📖 Propósito

Este directorio externaliza las condiciones soberanas del sistema como estado persistente verificable. No es configuración de aplicación — es la declaración soberana del sistema en cada arranque.

## 🏗️ Arquitectura

### Condiciones Constitucionales

#### foundation.json — [foundation] Condiciones Irreducibles
```json
{
  "status": "OK | DEGRADED | COMPROMISED",
  "identity_verified": true,
  "corpus_accessible": true,
  "ledger_available": true,
  "notes": []
}
```

- **OK**: Sistema operativo soberanamente
- **DEGRADED**: Operación limitada con advertencias
- **COMPROMISED**: Detiene todo el sistema — FoundationError
- **notes[]**: Registro de anomalías activas

#### scope.json — [scope] Perímetro Operativo
```json
{
  "name": "IMV_core_modules",
  "allowed_modules": ["grammar", "samu", "ledger", "chat", "main"],
  "status": "ACTIVE | EXCEEDED | UNDEFINED"
}
```

- **allowed_modules**: Módulos que pueden ejecutarse
- **ACTIVE**: Perímetro operativo normal
- **EXCEEDED**: Intento de ejecutar módulo no permitido — ScopeError
- **UNDEFINED**: scope no definido — ScopeError

#### term.json — [term] Horizonte Temporal
```json
{
  "label": "open",
  "status": "OPEN | ACTIVE | EXPIRED",
  "cycle_id": null
}
```

- **OPEN**: Sin fecha límite — operación continua
- **ACTIVE**: Ciclo con horizonte declarado
- **EXPIRED**: Ciclo cerrado soberanamente — TermError

### Configuración de Interfaz (Niveles 2-3)

#### api.json — Nivel 2: API Externa
```json
{
  "provider": "openai",
  "key": "sk-PONER-CLAVE-AQUI",
  "model": "gpt-4o-mini",
  "note": "Copiar como api.json y agregar clave real. NUNCA commitear api.json."
}
```

- **provider**: openai (compatible con Claude vía proxy, Groq)
- **key**: Clave API real (NUNCA versionar)
- **model**: gpt-4o-mini (más económico), gpt-4o, claude-3-sonnet
- **Activación**: Descomentar openai>=1.0.0 en requirements.txt

#### ollama.json — Nivel 3: Modelo Local
```json
{
  "model": "deepseek-coder:6.7b",
  "endpoint": "http://localhost:11434/api/generate",
  "note": "Copiar como ollama.json cuando Ollama esté instalado y modelo descargado."
}
```

- **model**: deepseek-coder:6.7b, mistral:7b, llama3:8b
- **endpoint**: http://localhost:11434/api/generate (Ollama default)
- **Hardware**: Ryzen 5 7600, 8GB+ RAM libre
- **Instalación**: `curl -fsSL https://ollama.ai/install.sh | sh`

## 🔄 Verificación Soberana

### verify_sovereign_conditions(module)
Función central decorada con `@lru_cache(maxsize=1)`:
- **Orden**: foundation → scope → term
- **Cache**: Una sola lectura de disco por sesión
- **Excepciones**: FoundationError, ScopeError, TermError
- **Fall-through**: Si cualquiera falla, sistema se detiene

### Limitación Intencional
El `@lru_cache` hace que cambios en config/ durante una sesión no sean detectados. Esto es intencional — la soberanía no se reconfigura en caliente. Para recargar: reiniciar el sistema.

## 🛡️ Seguridad

### Archivos Sensibles
```bash
# NUNCA commitear estos archivos:
api.json      # Contiene clave API real
ollama.json   # Configuración local específica
```

### Archivos Seguros
```bash
# Estos SÍ se versionan:
api.json.example      # Plantilla sin clave
ollama.json.example   # Plantilla genérica
.gitignore_note.txt   # Instrucciones de seguridad
```

### .gitignore Recomendado
```gitignore
# Configuración con claves reales
IMV/config/api.json
IMV/config/ollama.json

# Logs y datos (futuro)
IMV/logs/*.log
IMV/data/*.db-journal
```

## 🚀 Protocolo de Configuración

### Para Nivel 2 (API Externa)
```bash
# 1. Descomentar en requirements.txt:
# openai>=1.0.0

# 2. Instalar dependencia:
pip install openai

# 3. Crear configuración:
cp config/api.json.example config/api.json

# 4. Editar con clave real:
# {"provider": "openai", "key": "sk-...", "model": "gpt-4o-mini"}

# 5. Probar:
python main.py
DIRIME> quiero verificar el estado del sistema
# → Debe traducir vía API externa
```

### Para Nivel 3 (Modelo Local)
```bash
# 1. Instalar Ollama:
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Descargar modelo:
ollama pull deepseek-coder:6.7b

# 3. Crear configuración:
cp config/ollama.json.example config/ollama.json

# 4. Verificar Ollama activo:
curl http://localhost:11434/api/tags

# 5. Probar:
python main.py
DIRIME> necesito auditar la coherencia del sistema
# → Debe traducir vía Ollama local
```

## 📊 Estado por Defecto

### foundation.json (OK)
```json
{
  "status": "OK",
  "identity_verified": true,
  "corpus_accessible": true,
  "ledger_available": true,
  "notes": []
}
```

### scope.json (ACTIVE)
```json
{
  "name": "IMV_core_modules",
  "allowed_modules": ["grammar", "samu", "ledger", "chat", "main"],
  "status": "ACTIVE"
}
```

### term.json (OPEN)
```json
{
  "label": "open",
  "status": "OPEN",
  "cycle_id": null
}
```

## 🔧 Mantenimiento

### Verificación de Integridad
```bash
# Verificar que existan los tres archivos constitucionales:
ls config/foundation.json config/scope.json config/term.json

# Verificar sintaxis JSON:
python -m json.tool config/foundation.json
python -m json.tool config/scope.json
python -m json.tool config/term.json
```

### Expansión de Scope
Cuando se agrega un nuevo módulo:
```json
// scope.json
{
  "name": "IMV_core_modules",
  "allowed_modules": ["grammar", "samu", "ledger", "chat", "main", "nuevo_modulo"],
  "status": "ACTIVE"
}
```

### Ciclos Temporales
Para operación con horizonte definido:
```json
// term.json
{
  "label": "ciclo_2025_Q1",
  "status": "ACTIVE",
  "cycle_id": "2025-03-03_to_2025-06-03"
}
```

## 🎯 Principios Soberanos

1. **Externalización**: Las condiciones no viven solo en código
2. **Persistencia**: Sobreviven a reinicios del sistema
3. **Verificación**: Se validan en cada arranque
4. **Inmutabilidad**: No se reconfiguran en caliente
5. **Trazabilidad**: Cambios requieren reinicio explícito

---

**Para agentes AI**: Estos archivos definen el suelo soberano del sistema. foundation.json determina si el sistema puede arrancar. scope.json define qué puede ejecutar. term.json define por cuánto tiempo. api.json/ollama.json son mejoras de interfaz opcionales.
