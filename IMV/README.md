# IMV — Implementación Mínima Verificable

## 📖 Qué es IMV

IMV es el primer TOMO real de DIRIME. No es DIRIME completo — es la prueba verificada de que la constitución LACHO funciona como código ejecutable soberanamente.

### Relación exacta
- **LACHO**: lenguaje constitucional — gramática viva, bibliotecas, paradigmas, nudos
- **DIRIME**: plataforma operativa — dos nodos, HL FABRIC real, WEB3, Scheduler OS
- **IMV**: subconjunto mínimo de DIRIME que demuestra que LACHO es ejecutable

### Lo que IMV NO es
- HL FABRIC Hyperledger real (usa SQLite provisional)
- Dos nodos físicos (opera en nodo único)
- WEB3 activo
- Behavioral RAG completo (tiene auto_crystallize() mínimo)
- Scalar S ni Ψ(T) operativo
- BALLPAPER render soberano
- {DOGMA-VIRTUAL} activo
- UNICODE-CHINA

## 🏗️ Arquitectura IMV

Cuatro módulos en orden soberano de dependencia:

### IMV-1 — foundation.py
Condiciones irreducibles [foundation][scope][term]
- `verify_sovereign_conditions()` — validación de arranque
- Externalización en config/*.json

### IMV-2 — grammar.py
Validador de sentencias gramática viva LACHO
- `GrammarValidator` — 5 reglas + paradigmas
- `KEYWORDS_SYSTEM` — 8 keywords transversales
- `normalize_verb()` — normalización canónica

### IMV-3 — samu.py
Dirimencia soberana mínima (SAMU @ reducido)
- `Samu` — auditor soberano
- `Dispute` — registro de incoherencias
- `Scalar S` — métrica de coherencia

### IMV-4 — ledger.py
HL FABRIC provisional SQLite
- `HLFabric` — registro inmutable
- `auto_crystallize()` — Behavioral RAG mínimo
- `suggest_from_history()` — aprendizaje operador

### IMV-5 — chat.py
Interfaz AI — traductor canónico NL→LACHO
- 4 niveles de traducción (0→3)
- 20 patrones hardcodeados (Nivel 1)
- Stubs para API externa y Ollama (Niveles 2-3)

### IMV-0 — main.py
Orquestador soberano — punto de entrada
- `SovereignSystem` — inicialización y coordinación
- 3 modos: interactivo, --validate, --stats

## 🚀 Instalación y Uso

### Dependencias (solo las activas hoy)
```bash
python>=3.10
rich>=13.0.0
pydantic>=2.0.0
# sqlite3 viene con Python
```

### Instalación
```bash
git clone <repo>
cd DIRIME/IMV
pip install -r requirements.txt
python main.py
```

### Uso operativo
```bash
# Nivel 0: Gramática directa (recomendado)
DIRIME> TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]

# Nivel 1: 20 patrones hardcodeados
DIRIME> verificar el sistema
DIRIME> custodiar activo soberano
DIRIME> dirimir disputa activa

# Validación directa
python main.py --validate "texto LACHO"

# Estadísticas
python main.py --stats
```

## 🔄 Ciclo Soberano Completo

```
operador escribe → chat.py traduce → grammar.py valida → samu.py dirime → ledger.py registra → resultado retorna
```

### Condición de éxito IMV
Una sentencia LACHO real pasa por los cuatro módulos y el resultado es trazable, auditable y reproducible.

### Verificación mínima
```bash
python main.py --validate "TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]"
python main.py --stats
```

## 📁 Estructura del Directorio

```
IMV/
├── main.py              # Orquestador soberano (IMV-0)
├── requirements.txt     # Dependencias soberanas
├── config/              # Externalización soberana
│   ├── foundation.json  # [foundation] condiciones
│   ├── scope.json       # [scope] módulos permitidos
│   ├── term.json        # [term] horizonte temporal
│   ├── api.json.example # API externa (plantilla)
│   └── ollama.json.example # Modelo local (plantilla)
├── core/                # Módulos soberanos
│   ├── foundation.py    # IMV-1: condiciones irreducibles
│   ├── grammar.py       # IMV-2: validador gramática viva
│   ├── samu.py          # IMV-3: dirimencia soberana
│   └── ledger.py        # IMV-4: HL FABRIC provisional
├── interface/           # Interfaz con operador
│   └── chat.py          # IMV-5: traductor NL→LACHO
├── data/                # Datos persistentes
│   └── sovereign.db     # SQLite HL FABRIC
├── logs/                # Logs soberanos (futuro)
└── tests/               # Tests soberanos (futuro)
```

## 📊 Métricas y Estado

### Scalar S
- **Propósito**: Métrica de coherencia soberana
- **Rango**: [0,1] donde 1 = coherencia perfecta
- **Cálculo**: S = valid_ratio × (1 - red_regret_weight)
- **Umbral**: S ≥ 0.7 para operación soberana

### Behavioral RAG Mínimo
- **auto_crystallize()**: cristaliza verbos VALID con frecuencia ≥10
- **suggest_from_history()**: sugiere library/knot basado en historial
- **Activación**: automática en chat.py cuando hay historial suficiente

### Paradigmas de Validación
Cada biblioteca tiene régimen diferenciado:
- **TRUST**: imperativo (ordena, verifica, declara)
- **SOCIAL**: declarativo (describe, reporta, notifica)
- **CRYPTO**: funcional (transforma entrada en salida)
- **WORK**: bajo nivel (toca hardware/OS)
- **SAMU**: alto nivel (abstracción máxima)
- **GATE**: scripts (secuencia de estados)
- **METHOD**: enumerables (operadores formales)
- **ACTIVITY**: nivel medio (ciclos UF[H##])
- **STACKING**: orientado a objetos (cristaliza, persiste)

## 🛡️ Seguridad y Configuración

### Configuración Soberana
Los archivos config/*.json externalizan las condiciones soberanas:
- **foundation.json**: estado del sistema
- **scope.json**: módulos permitidos
- **term.json**: horizonte temporal

### Claves API (Nivel 2)
```bash
cp config/api.json.example config/api.json
# Editar con clave real, NUNCA commitear api.json
```

### Modelo Local (Nivel 3)
```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull deepseek-coder:6.7b
cp config/ollama.json.example config/ollama.json
```

## 🧪 Testing

### Test básico de arranque
```bash
python main.py --validate "TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]"
# Debe retornar VALID sin errores
```

### Test de estadísticas
```bash
python main.py --stats
# Debe mostrar transacciones, cristales, Scalar S
```

### Test de módulos individuales
```bash
python -m core.foundation
python -m core.grammar
python -m core.samu
python -m core.ledger
```

## 📈 Próxima Versión (v0.2.0)

### Implementado en código
- ✅ Bug fetchone()→fetchall() en ledger.py
- ✅ scalar_s property en samu.py
- ✅ suggest_from_history() en ledger.py
- ✅ Behavioral RAG activo en chat.py
- ✅ _validate_by_paradigm() en grammar.py

### Por implementar
- 🔄 Scalar S en stats/BALLPAPER
- 🔄 Versión actualizada a 0.2.0
- 🔄 Tests automatizados
- 🔄 Logs estructurados

## 🎯 Objetivo

IMV demuestra que la soberanía es posible con tecnología existente hoy. Un sistema donde:

- La verdad es local (no depende de validadores externos)
- La autoridad es soberana (las reglas son constitucionales)
- El lenguaje es operativo (LACHO ejecuta sin intermediarios)

DIRIME completo es el horizonte. IMV es la prueba verificable de que ese horizonte es alcanzable.

---

**Estado actual**: IMV v0.1.0 — Ciclo soberano completo operativo.  
**Próximo**: v0.2.0 — Métricas activas + validación diferenciada.
