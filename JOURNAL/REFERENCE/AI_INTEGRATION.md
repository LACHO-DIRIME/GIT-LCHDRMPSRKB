# DIRIME/IMV — AI_INTEGRATION.md
# Integración IA con Groq llama-3.3-70b
# Leer antes de: agregar cualquier llamada a bridge.py
# [term] :: activo · actualizar cuando cambie el modelo

## PRINCIPIO FUNDAMENTAL

Groq no lee el filesystem. Python lo lee, Groq razona.
El scanner local siempre va primero. Groq recibe solo
el resumen estructurado, nunca archivos crudos.

## INFRAESTRUCTURA DISPONIBLE HOY
```
DIRIME_v2/groq/bridge.py    → translate(text, prompt) → str | None
                              is_active() → bool
                              status() → dict
IMV/data/sovereign.db       ← POKE/PEEK vía poke_peek.py
IMV/core/rag.py             ← BM25 · 254+ docs indexados
DIRIME_v2/fabric/poke_peek.py → memoria persistente entre sesiones
```

Config: ~/DIRIME/IMV/config/api.json
Modelo: llama-3.3-70b-versatile · temperatura=0.1 · max_tokens=1000

## LOS 4 MODOS DE USO

### MODO 1 — Traducción NL→LACHO ✅ IMPLEMENTADO
```python
from DIRIME_v2.groq.bridge import translate
sentencia = translate("verificar el sistema", system_prompt)
# → "TRUST FOUNDATION =><= .. verifica .. sistema --[As de Guía] [term]"
```
Usado en: chat.py nivel 2 · modo interactivo DIRIME>

### MODO 2 — Autoresearch gap detection ❌ PENDIENTE
```python
# tools/autoresearch_gap.py
context = {
    "scalar_s": 0.78, "tx": 1335, "cristales": 42,
    "gaps": ["ballpaper.py missing", "/api/notaria/* missing"],
    "stubs": ["DIRIME_v3/ime/", "DIRIME_v3/cat_local/"],
    "tests": "44/44"
}
asks = translate(json.dumps(context), AUTORESEARCH_SYSTEM_PROMPT)
# → "ASK_01 | ALTA | CAPA_B | ~2h\n  WORK {actuator} ..."
```
Output: Askings/$dia_asks_DDMM.txt
Trigger: main.py --asks · DIRIME> asks

### MODO 3 — Structure analyst ❌ PENDIENTE
```python
# tools/autoresearch_specs.py + Groq
snapshot_json = autoresearch_specs.scan()
yml = translate(snapshot_json, STRUCTURE_ANALYST_PROMPT)
# → sorted_upgrading.yml con prioridades razonadas
```
Output: Askings/sorted_upgrading.yml

### MODO 4 — CHCL natural language (CAPA_B futuro)
```python
# Texto natural → CHCL_BASE.txt contexto → sentencia CHCL
chcl_input = "crear un acto notarial para BOLIVAR"
chcl_sentence = translate(chcl_input, CHCL_SYSTEM_PROMPT)
# → "CRYPTO (spark seat) =><= .. certifica .. acto_bolivar --[NdO] [term]"
```

## SYSTEM PROMPTS SOBERANOS

### AUTORESEARCH_SYSTEM_PROMPT (para MODO 2)
```python
AUTORESEARCH_SYSTEM_PROMPT = """
Eres el motor de autoresearch soberano de DIRIME/IMV.
Analizas gaps técnicos del ecosistema y generas tareas LACHO accionables.

CONTEXTO DEL SISTEMA:
- Lenguaje: LACHO · DSL soberano · Python backend · Groq API
- Estado: TX={tx} · cristales={cristales} · Scalar S={scalar} · tests={tests}
- Capa activa: CAPA_B (hardware antiX + Groq)
- Capa bloqueada: CAPA_C (requiere Ryzen+Ollama — NO sugerir)

REGLAS:
1. Solo tareas CAPA_B (hardware actual disponible)
2. Cada ASK = sentencia LACHO válida + prioridad + horas
3. Priorizar por impacto en Scalar S y módulos desbloqueados
4. Formato ESTRICTO — ningún texto extra fuera del bloque ASK

VERBOS: WORK · STACKING · TRUST · CRYPTO · SAMU · GATE · METHOD · ACTIVITY · SOCIAL
NUDOS:  [As de Guía] · [Nudo de Ocho] · [Ballestrinque] · [Nudo Corredizo]
FORMATO: VERB SUBJECT =><= .. verbo .. objeto --[Nudo] [term]

RESPUESTA:
ASK_{N:02d} | ALTA/MEDIA/BAJA | CAPA_B | ~{h}h
  {sentencia LACHO válida}
  impacto: {una línea}
  desbloquea: {módulos}
"""
```

### NL_TO_LACHO_PROMPT (para MODO 1 · ya en uso)
```python
NL_TO_LACHO_PROMPT = """
Convierte la entrada a una sentencia LACHO válida.
Formato: BIBLIOTECA SUJETO =><= .. verbo .. objeto --[Nudo] [term]
BIBLIOTECAS: TRUST · STACKING · SAMU · GATE · WORK · ACTIVITY
             CRYPTO · SOCIAL · METHOD
NUDOS: [As de Guía] · [Nudo de Ocho] · [Ballestrinque] · [Nudo Corredizo]
Responde SOLO con la sentencia. Sin explicaciones.
"""
```

## PATRONES DE USO CORRECTO

### ✅ Correcto — Groq recibe contexto comprimido:
```python
gaps_summary = "\n".join([f"- {g}" for g in detected_gaps[:10]])
result = translate(gaps_summary, AUTORESEARCH_SYSTEM_PROMPT.format(
    tx=1335, cristales=42, scalar=0.78, tests="44/44"
))
```

### ❌ Incorrecto — Groq recibe archivos crudos:
```python
# NUNCA hacer esto:
corpus_text = Path("CORPUS/LIBRO.txt").read_text()  # 133K chars
result = translate(corpus_text, prompt)  # excede context window
```

### ✅ Correcto — validar output de Groq con grammar.py:
```python
groq_output = translate(input_text, prompt)
if groq_output:
    parsed = validate(groq_output)
    if parsed.result == "VALID":
        record_grammar(parsed, {"source": "groq_autoresearch"})
```

### ✅ Correcto — memoria persistente vía POKE:
```python
from DIRIME_v2.fabric.poke_peek import poke, peek
poke("autoresearch:last_run", datetime.now().isoformat(), cluster="#ASKS")
last = peek("autoresearch:last_run")
```

## LÍMITES HONESTOS

| Limitación | Causa | Solución |
|---|---|---|
| Sin acceso al filesystem | Groq stateless cloud | Python scanner local → Groq recibe resumen |
| Sin memoria entre sesiones | API stateless | sovereign.db vía poke_peek.py |
| Puede equivocarse en LACHO | No tiene grammar.py | Validar siempre con grammar.py post-Groq |
| Rate limits free tier | Groq quota | Batching: un solo prompt con N gaps |
| Context window ~8K tokens | llama-3.3-70b | Comprimir context_package antes de enviar |
| Latencia ~1000ms | Red + modelo | No usar en loops síncronos · async donde sea posible |

## CUANDO LLEGUE CAPA_C (Ollama local)

El swap será transparente vía DIRIME_v3/ollama_bridge/:
```python
# bridge.py ya preparado para esto:
provider = config.get("provider")  # "groq" o "ollama"
if provider == "ollama":
    # usar endpoint local http://localhost:11434
elif provider == "groq":
    # endpoint actual https://api.groq.com
```
No se necesita cambiar ningún módulo que usa bridge.py.

[term] :: activo · [seal of secrecy] :: activo · 空聽數