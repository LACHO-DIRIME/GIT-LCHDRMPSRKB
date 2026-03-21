"""
DIRIME IMV — chat.py
Interfaz soberana de entrada — cuatro niveles de traducción.

NIVEL 0 (activo): operador escribe gramática LACHO directamente.
  Sin dependencias externas. Ciclo completo operativo hoy.

NIVEL 1 (activo, limitado): 20 patrones de string hardcodeados.
  _translate_to_lacho() — funciona para palabras clave definidas.
  No es traducción de lenguaje natural real.

NIVEL 2 (pendiente): traducción vía API externa (OpenAI / Claude / Groq).
  Requiere: internet + clave API + implementar _translate_via_api().
  Hardware actual es suficiente.

NIVEL 3 (futuro): traducción vía modelo local Ollama.
  Requiere: 8GB+ RAM libre, Ryzen 5 7600 o equivalente.
  Sin internet, sin costo por llamada.

Referencia canónica:
  BIBLIO-SOURCES(DIRIME-LINUX_CHAT-AI-SOBERANO).txt
  BIBLIO-SOURCES(DIRIME-IMV_CHAT).txt
"""

from __future__ import annotations
import sys
import time
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

# Garantizar que core/ es encontrado sin importar desde dónde se ejecuta python
_IMV_DIR = Path(__file__).parent.parent
if str(_IMV_DIR) not in sys.path:
    sys.path.insert(0, str(_IMV_DIR))

from core.foundation import verify_sovereign_conditions
from core.grammar import validate, ParsedSentence
from core.samu import audit, verify_coherence
from core.ledger import record_grammar, suggest_from_history


# ── Estados del Chat ───────────────────────────────────────────────
class ChatState(Enum):
    IDLE = "IDLE"                    # Esperando entrada
    PROCESSING = "PROCESSING"        # Procesando soberanamente
    RESPONDING = "RESPONDING"        # Generando respuesta
    ERROR = "ERROR"                  # Error soberano


# ── Tipos de respuesta ─────────────────────────────────────────────
class ResponseType(Enum):
    VALIDATION = "VALIDATION"        # Resultado de validación
    DIRIMENCE = "DIRIMENCE"          # Decisión SAMU
    ERROR = "ERROR"                  # Error procesamiento
    HELP = "HELP"                    # Ayuda soberana


# ── Modelo de mensaje ───────────────────────────────────────────────
@dataclass
class ChatMessage:
    user_input: str
    response_type: ResponseType = ResponseType.VALIDATION
    response_content: str = ""
    processing_time_ms: int = 0
    sovereign_verified: bool = False
    timestamp: float = field(default_factory=time.time)


# ── Chat AI soberano ───────────────────────────────────────────────
class SovereignChat:
    """
    Chat AI interface mínima — traductor canónico soberano.
    
    No es un chatbot convencional. Es un traductor canónico:
    - Natural language → Gramática viva LACHO
    - Gramática viva LACHO → Natural language
    
    Referencia: BIBLIO-SOURCES(DIRIME-LINUX_CHAT-AI-SOBERANO).txt
    """

    def __init__(self):
        self.state = ChatState.IDLE
        self.session_history: list[ChatMessage] = []
        self._last_translation_was_default = False

    def _detect_input_type(self, user_input: str) -> str:
        """
        Detecta si el input es comando, gramática LACHO o natural."""
        user_input_stripped = user_input.strip()

        # Comandos
        if user_input_stripped.lower() in ["help","ayuda","?","h"]:
            return "help"
        
        # Comandos del sistema
        cmd_check = user_input_stripped.lower()
        if cmd_check in {"verbos", "verbs", "bibliotecas", "libs", 
                         "nudos", "knots", "timeline", "dias", 
                         "cristales", "crystals", "cristals", "cr", "db", "ledger",
                         "switch", "tomo", "tomos", "unicode"} \
           or cmd_check.startswith("switch "):
            return "command"

        # Gramática LACHO — tiene =><=
        if "=><=" in user_input_stripped:
            return "lacho"

        # Posible intento de gramática LACHO sin =><=
        # Si empieza con palabra en mayúsculas seguida de
        # otra palabra o módulo — tratar como lacho para
        # que el validador dé el error correcto
        first_word = user_input_stripped.split()[0] if user_input_stripped else ""
        VALID_LIBS = ["TRUST","SOCIAL","CRYPTO","WORK","SAMU",
                      "ACTIVITY","GATE","STACKING","METHOD"]
        # Verificar si la primera palabra es una biblioteca válida o similar
        if first_word.upper() in VALID_LIBS or any(first_word.upper().startswith(lib) for lib in VALID_LIBS):
            return "lacho"
        
        # Si contiene [biblioteca] es probablemente LACHO
        if any(lib in user_input for lib in ["TRUST", "SOCIAL", "ACTIVITY", "WORK", "SAMU"]):
            return "lacho"
        
        # Si contiene .. o --[ o [term] es probablemente LACHO
        if ".." in user_input or "--[" in user_input or "[term]" in user_input:
            return "lacho"

        # Natural language
        return "natural"

    def _translate_to_lacho(self, natural_text: str) -> str:
        """
        Traduce natural language a gramática LACHO.
        
        IMV mínimo: detección de patrones básicos.
        En producción: modelo de lenguaje entrenado en corpus LACHO.
        """
        text_lower = natural_text.lower()
        
        # Cascada soberana de traducción: nivel 3 → 2 → 1 → 0
        # Nivel 3: modelo local Ollama (si configurado y disponible)
        ollama_result = self._translate_via_ollama(natural_text)
        if ollama_result and "=><=".strip() in ollama_result:
            return ollama_result

        # Nivel 2: API externa (si configurada)
        api_result = self._translate_via_api(natural_text)
        if api_result and "=><=".strip() in api_result:
            return api_result

        # Nivel 1: 20 patrones hardcodeados (activo siempre como fallback)
        # ... continúa el código existente de patrones
        
        # Behavioral RAG: consultar historial antes de aplicar patrones fijos
        words = natural_text.strip().split()
        first_verb = words[0].lower() if words else ""
        try:
            suggestion = suggest_from_history(first_verb)
            if suggestion:
                library = suggestion.get('library', 'TRUST')
                knot = suggestion.get('knot', 'As de Guía')
                obj = "_".join(words[1:3]) if len(words) > 1 else "objeto_soberano"
                return f"{library} FOUNDATION =><= .. {first_verb} .. {obj} --[{knot}] [term]"
        except Exception:
            pass  # RAG falla silenciosamente, continúa con patrones fijos
        
        # Patrones existentes
        if "verificar" in text_lower or "validar" in text_lower:
            return "TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]"
        if "iniciar" in text_lower or "empezar" in text_lower:
            return "ACTIVITY UF[H01] =><= .. inicia .. tarea_inicial --[As de Guía] [term]"
        if "detener" in text_lower or "parar" in text_lower:
            return "WORK {brake} =><= .. detiene .. accion_critica --[Nudo de Ocho] [term]"
        if "dirimir" in text_lower or "decidir" in text_lower:
            return "SAMU @ =><= .. dirime .. disputa_activa --[Ballestrinque] [term]"
        if "custodiar" in text_lower or "guardar" in text_lower:
            return "WORK {doorman-mobile} =><= .. custodia .. activo_soberano --[Nudo de Ocho] [term]"
        if "cristalizar" in text_lower or "registrar" in text_lower:
            return "STACKING UF[H52] =><= .. cristaliza .. patron_verificado --[Nudo Corredizo] [term]"
        if "lanzar" in text_lower or "emitir" in text_lower:
            return "SOCIAL {launch-bot} =><= .. lanza .. accion_soberana --[As de Guía] [term]"
        if "proteger" in text_lower or "bloquear" in text_lower:
            return "CRYPTO (shield seat) =><= .. protege .. dispositivo_activo --[As de Guía] [term]"
        if "autorizar" in text_lower or "activar" in text_lower:
            return "CRYPTO (spark seat) =><= .. autoriza .. acceso_permitido --[As de Guía] [term]"
        
        # Nuevos patrones agregados
        if "invertir" in text_lower or "comprar" in text_lower:
            return "ACTIVITY UF[H30] =><= .. invierte .. capital_soberano --[Nudo de Ocho] [term]"

        if "esperar" in text_lower or "aguardar" in text_lower:
            return "GATE UF[H05] =><= .. espera .. momento_soberano --[Ballestrinque] [term]"

        if "conectar" in text_lower or "enlazar" in text_lower:
            return "CRYPTO (link seat) =><= .. conecta .. canal_soberano --[Nudo de Ocho] [term]"

        if "monitorear" in text_lower or "auditar" in text_lower:
            return "SAMU @ =><= .. audita .. estado_sistema --[Nudo de Rizo] [term]"

        if "aprender" in text_lower or "recordar" in text_lower:
            return "STACKING UF[H48] =><= .. aprende .. patron_verificado --[Nudo Corredizo] [term]"

        if "fluir" in text_lower or "transitar" in text_lower:
            return "GATE UF[H56] =><= .. transita .. zipper_activo --[Nudo Corredizo] [term]"

        if "resolver" in text_lower or "cerrar" in text_lower:
            return "GATE UF[H06] =><= .. resuelve .. tension_activa --[Nudo de Rizo] [term]"

        if "declarar" in text_lower or "notariar" in text_lower:
            return "TRUST [command] =><= .. declara .. acto_soberano --[As de Guía] [term]"

        if "sellar" in text_lower or "certificar" in text_lower:
            return "WORK {door-afternoon} =><= .. sella .. documento_verificado --[Nudo de Ocho] [term]"

        if "suspender" in text_lower or "bloquear" in text_lower:
            return "GATE UF[H05] =><= .. suspende .. acceso_activo --[Ballestrinque] [term]"
        
        # Input no reconocido — marcar para feedback
        self._last_translation_was_default = True
        words = natural_text.strip().split()
        verb = words[0].lower() if words else "procesa"
        obj = "_".join(words[1:3]) if len(words) > 1 else "objeto_soberano"
        return f"TRUST FOUNDATION =><= .. {verb} .. {obj} --[As de Guía] [term]"

    def _translate_via_api(self, natural_text: str) -> str | None:
        """
        NIVEL 2 — Traducción vía Groq API.
        Estado: ACTIVO cuando existe config/api.json con provider=groq.

        Retorna: sentencia LACHO generada, o None si falla/no configurado.
        """
        try:
            import json
            import httpx
            from pathlib import Path

            api_cfg = Path(__file__).parent.parent / "config" / "api.json"
            if not api_cfg.exists():
                return None

            with open(api_cfg) as f:
                cfg = json.load(f)

            if cfg.get("provider") != "groq":
                return None

            api_key = cfg.get("key", "")
            if not api_key or api_key.startswith("REEMPLAZAR"):
                return None

            # Cargar referencia gramatical del corpus
            corpus_path = Path(__file__).parent.parent.parent / "CORPUS"
            grammar_doc = ""
            grammar_file = corpus_path / "BIBLIO-SOURCES(GRAMATICA VIVA).txt"
            if grammar_file.exists():
                grammar_doc = grammar_file.read_text(encoding="utf-8",
                                                      errors="ignore")[:2000]

            system_prompt = """Sos un traductor de lenguaje natural a gramática LACHO.
Fuentes doctrinales prioritarias (peso doble en interpretación):
- COGNITIVO_03: taxonomía viva e inventario soberano del sistema
- COGNITIVO_04: fenomenología soberana, cómo se habita LACHO en vivo
- BIBLIO-SOURCES(HEADCAT): director de salida WU, gobierno soberano
- BIBLIO-SOURCES(FLYBOT): agente de ejecución LACHO→HEADCAT→FLYBOT→HARDWARE
- SOURCE&ASSET%WORTH: iconografía completa ELPULSAR y PULSING
- BIBLIOTECAS_MADRE_LACHO: BALLPAPER + UNICODE programable

FORMATO OBLIGATORIO — exactamente este orden:
BIBLIOTECA SUJETO =><= .. verbo .. objeto --[Nudo] [term]

REGLAS ABSOLUTAS:
1. Responder SOLO con la sentencia. Sin explicación. Sin markdown. Sin comillas.
2. El verbo SIEMPRE entre dos puntos: .. verbo ..
3. SIEMPRE terminar con --[Nudo] [term]
4. NUNCA usar la palabra BIBLIOTECA literalmente
5. NUNCA usar la palabra Sujeto literalmente
6. NUNCA usar la palabra Objeto literalmente
7. Elegir biblioteca y sujeto del listado de abajo

BIBLIOTECAS Y SUJETOS VÁLIDOS:
  TRUST    → FOUNDATION [foundation] [scope] [term] [command] [management]
  WORK     → {actuator} {brake} {doorman-mobile} {door-afternoon} {green-knowledge}
  CRYPTO   → (spark seat) (shield seat) (key seat) (flow seat) (link seat) (ignition seat)
  SAMU     → @ #rise #set
  ACTIVITY → UF[H01] UF[H29] UF[H30] UF[H51] UF[H52] UF[H57]
  GATE     → UF[H05] UF[H56] UF[H06]
  STACKING → UF[H02] UF[H04] UF[H23] UF[H48] UF[H52] UF[H63]
  SOCIAL   → {launch-bot} {chair} {scheduler} {drip} {relay} {masking}
  METHOD   → <equation> <if> <operator_flow> <stat_onto> <psi_spin>

VERBOS CANÓNICOS POR BIBLIOTECA:
  TRUST    → verifica / declara / sostiene / autoriza / limita
  WORK     → materializa / ejecuta / detiene / custodia / sella
  CRYPTO   → autoriza / certifica / protege / firma / conecta
  SAMU     → dirime / audita / modera / registra / activa
  ACTIVITY → penetra / emerge / completa / inicia / transita
  GATE     → bloquea / abre / filtra / contiene / permite
  STACKING → cristaliza / inmutabiliza / preserva / archiva / sella
  SOCIAL   → lanza / planifica / conecta / transmite / enmascara
  METHOD   → define / formaliza / opera / calcula / estructura

REGLA: Preferir verbos canónicos. Si el input sugiere otro,
usar el equivalente más próximo de la misma biblioteca.

NUDOS VÁLIDOS (elegir el más apropiado):
  As de Guía     → acción exitosa, verificación, estado correcto
  Nudo de Ocho   → registro permanente, cristalización, inmutable
  Ballestrinque  → tensión activa, evaluación, conflicto
  Nudo Corredizo → riesgo, alerta, atención requerida
  Nudo de Rizo   → cierre de ciclo, transición

EJEMPLOS OBLIGATORIOS — aprender exactamente este formato:

Input: necesito verificar el estado del sistema
Output: TRUST FOUNDATION =><= .. verifica .. estado_sistema --[As de Guía] [term]
Input: registrar documento legal en el sistema
Output: STACKING UF[H52] =><= .. archiva .. documento_legal --[Nudo de Ocho] [term]
Input: auditar coherencia de la gramática
Output: SAMU @ =><= .. audita .. coherencia_gramatical --[As de Guía] [term]
Input: cerrar el período soberano del día
Output: SAMU #set =><= .. dirime .. periodo_soberano --[Nudo de Rizo] [term]
Input: evaluar riesgo de lanzamiento de memecoin
Output: CRYPTO (spark seat) =><= .. certifica .. riesgo_lanzamiento_memecoin --[Ballestrinque] [term]
Input: registrar documento legal en el sistema
Output: STACKING UF[H52] =><= .. archiva .. documento_legal --[Nudo de Ocho] [term]
Input: auditar coherencia de la gramática
Output: SAMU @ =><= .. audita .. coherencia_gramatical --[As de Guía] [term]
Input: cerrar el período soberano del día
Output: SAMU #set =><= .. dirime .. periodo_soberano --[Nudo de Rizo] [term]
Input: evaluar riesgo de lanzamiento de memecoin
Output: CRYPTO (spark seat) =><= .. certifica .. riesgo_lanzamiento_memecoin --[Ballestrinque] [term]

Input: quiero registrar una decisión en el ledger
Output: SAMU @ =><= .. audita .. decision_soberana --[Nudo de Ocho] [term]

Input: el sistema detectó una anomalía en el canal de flujo
Output: CRYPTO (flow seat) =><= .. audita .. anomalia_canal --[Ballestrinque] [term]

Input: necesito planificar el ciclo de memecoins para esta semana
Output: SOCIAL {scheduler} =><= .. planifica .. ciclo_memecoins --[As de Guía] [term]

Input: detener la operación de riesgo inmediatamente
Output: WORK {brake} =><= .. detiene .. operacion_riesgo --[Nudo Corredizo] [term]

Input: custodiar el activo soberano con protección máxima
Output: CRYPTO (shield seat) =><= .. protege .. activo_soberano --[As de Guía] [term]

Input: iniciar el ciclo semanal soberano
Output: SAMU #rise =><= .. activa .. ciclo_semanal --[As de Guía] [term]

Input: registrar cristal verificado en stacking
Output: STACKING UF[H52] =><= .. inmutabiliza .. cristal_verificado --[Nudo de Ocho] [term]

Input: lanzar bot de mercado para memecoins
Output: SOCIAL {launch-bot} =><= .. lanza .. bot_memecoins --[As de Guía] [term]

Input: evaluar estrategia bajo tensión activa
Output: CRYPTO (spark seat) =><= .. certifica .. estrategia_tension --[Ballestrinque] [term]

Input: certificar acto notarial
Output: CRYPTO (spark seat) =><= .. certifica .. acto_notarial --[As de Guía] [term]

Input: sellar documento soberano
Output: STACKING UF[H63] =><= .. sella .. documento_soberano --[Nudo de Ocho] [term]

Input: esperar reunión de partes
Output: GATE UF[H05] =><= .. espera .. partes_reunidas --[Ballestrinque] [term]

Input: declarar acto ante notario
Output: TRUST [command] =><= .. declara .. acto_notarial --[As de Guía] [term]

Input: registrar hash en blockchain notarial
Output: STACKING UF[H63] =><= .. inmutabiliza .. hash_notarial --[Nudo de Ocho] [term]

Input: evaluar estrategia bajo tensión activa
Output: SAMU @ =><= .. dirime .. estrategia_activa --[Ballestrinque] [term]"""

            # IME Modo RAG — enriquecer prompt con ejemplos del corpus
            try:
                from core.rag import get_rag_context
                rag_context = get_rag_context(natural_text)
                if rag_context:
                    system_prompt = system_prompt + "\n\n" + rag_context
            except Exception:
                pass  # RAG falla silenciosamente — Groq funciona igual

            response = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": cfg.get("model", "llama-3.3-70b-versatile"),
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": natural_text}
                    ],
                    "max_tokens": cfg.get("max_tokens", 150),
                    "temperature": cfg.get("temperature", 0.1),
                },
                timeout=10.0
            )

            if response.status_code != 200:
                return None

            data = response.json()
            result = data["choices"][0]["message"]["content"].strip()

            # Validación mínima: debe contener =><=  y [term]
            if "=><=".strip() in result and "[term]" in result:
                return result

            return None

        except Exception:
            return None  # cualquier fallo → volver a patrones fijos

    def _translate_via_ollama(self, natural_text: str) -> str | None:
        """
        NIVEL 3 — Traducción vía modelo local Ollama.
        Estado: ACTIVO - detección automática de modelos.
        """
        try:
            import httpx, json
            from pathlib import Path
            cfg_path = Path(__file__).parent.parent / "config" / "ollama.json"
            cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
            host = cfg.get("host", "http://localhost:11434")
            model = cfg.get("model", "qwen2.5:7b")

            # Verificar que Ollama responde
            ping = httpx.get(f"{host}/api/tags", timeout=2.0)
            if ping.status_code != 200:
                return None

            # Verificar que el modelo existe
            models = [m["name"] for m in ping.json().get("models", [])]
            if not any(model in m for m in models):
                return None

            system_prompt_ollama = "Traducí a gramática LACHO: BIBLIOTECA SUJETO =><= .. verbo .. objeto --[Nudo] [term]. Solo la sentencia, sin explicación."
            response = httpx.post(
                f"{host}/api/generate",
                json={"model": model, "prompt": system_prompt_ollama + "\n\nInput: " + natural_text,
                      "stream": False},
                timeout=30.0
            )
            if response.status_code != 200:
                return None
            result = response.json().get("response", "").strip()
            return result if ("=><=".strip() in result and "[term]" in result) else None
        except Exception:
            return None

    def _format_validation_response(self, parsed: ParsedSentence) -> str:
        """Formatea respuesta de validación gramatical."""
        lines = [
            f"🔍 **VALIDACIÓN GRAMATICAL**",
            f"**Resultado**: {parsed.result.value}",
            f"**Biblioteca**: {parsed.library.value}",
            f"**Sujeto**: {parsed.subject or '—'}",
            f"**Verbo**: {parsed.verb or '—'}",
            f"**Objeto**: {parsed.obj or '—'}",
            f"**Nudo**: {parsed.knot or '—'}",
            f"**[term]**: {'✅ Presente' if parsed.term_present else '❌ AUSENTE'}",
        ]
        
        if parsed.errors:
            lines.append(f"\n❌ **Errores**:")
            for error in parsed.errors:
                lines.append(f"   • {error}")
            from core.grammar import _validator
            suggestion = _validator.suggest_correction(parsed)
            lines.append(f"\n💡 **Sugerencia**:")
            lines.append(f"   {suggestion}")
        
        if parsed.warnings:
            lines.append(f"\n⚠️ **Avisos**:")
            for warning in parsed.warnings:
                lines.append(f"   • {warning}")
        
        return "\n".join(lines)

    def _format_help_response(self) -> str:
        return """
🤖 **DIRIME IMV — AYUDA SOBERANA**

**Comandos del sistema:**
  help / ?    — esta ayuda
  stats       — estadísticas del ledger con ratio soberano
  status      — estado de la sesión actual
  quit        — cerrar soberanamente

**Modo 1 — Gramática LACHO directa (recomendado):**
  BIBLIOTECA Sujeto =><= .. verbo .. Objeto --[Nudo] [term]

  verificar / validar    → TRUST FOUNDATION
  iniciar / empezar      → ACTIVITY UF[H01]
  detener / parar        → WORK {brake}
  dirimir / decidir      → SAMU @
  custodiar / guardar    → WORK {doorman-mobile}
  cristalizar / registrar→ STACKING UF[H52]
  lanzar / emitir        → SOCIAL {launch-bot}
  proteger / bloquear    → CRYPTO (shield seat)
  autorizar / activar    → CRYPTO (spark seat)
  invertir / comprar     → ACTIVITY UF[H30]
  esperar / aguardar     → GATE UF[H05]
  conectar / enlazar     → CRYPTO (link seat)
  monitorear / auditar   → SAMU @
  aprender / recordar    → STACKING UF[H48]
  fluir / transitar      → GATE UF[H56]
  resolver / cerrar      → GATE UF[H06]
  declarar / notariar    → TRUST [command]
  sellar / certificar    → WORK {door-afternoon}
  suspender / bloquear   → GATE UF[H05]

**GRAMÁTICA LACHO DIRECTA:**
  BIBLIOTECA Sujeto =><= .. VERBO .. OBJETO --[Nudo] [term]

**LAS 9 BIBLIOTECAS DISPONIBLES:**
  TRUST    → [objeto] con corchetes
  WORK     → {objeto} con llaves
  CRYPTO    → (objeto) con paréntesis
  SAMU      → @/#/$ símbolo
  ACTIVITY  → UF[H##] hexagrama
  GATE      → UF[H##] hexagrama
  STACKING  → UF[H##] hexagrama
  SOCIAL    → {objeto} con llaves
  METHOD    → <objeto> con ángulos

**LOS 5 NUDOS CANÓNICOS:**
  As de Guía · Nudo de Ocho · Ballestrinque
  Nudo Corredizo · Nudo de Rizo

**ERRORES MÁS COMUNES:**
  • Falta [term] al final → INVALID
  • Falta --[Nudo]        → INVALID
  • Falta =><= en medio   → INVALID (cascada)
  • Biblioteca inválida   → INVALID con sugerencia
  • Espacio en -- [Nudo]  → WARNING
  • Delimitadores mixtos   → WARNING

**EJEMPLOS COMPLETOS:**
  TRUST FOUNDATION =><= .. verifica .. scope --[As de Guía] [term]
  WORK {door-mobile} =><= .. custodia .. activo --[Nudo de Ocho] [term]
  CRYPTO (key seat) =><= .. autoriza .. acceso --[Ballestrinque] [term]
  SAMU @ =><= .. dirime .. disputa --[Nudo de Rizo] [term]
  ACTIVITY UF[H42] =><= .. penetra .. tarea --[As de Guía] [term]
  GATE UF[H05] =><= .. suspende .. acceso --[Ballestrinque] [term]
  STACKING UF[H48] =><= .. cristaliza .. patron --[Nudo Corredizo] [term]
  SOCIAL {launch-bot} =><= .. lanza .. bot --[As de Guía] [term]
  METHOD <equation> =><= .. calcula .. variable --[Nudo de Ocho] [term]

**PRINCIPIOS SOBERANOS:**
  • foundation → condiciones irreducibles de existencia
  • scope      → perímetro de operación declarado
  • term       → horizonte temporal activo
  • ledger     → registro inmutable de transacciones
  • SAMU       → dirimencia soberana de disputas

**ESTRUCTURA DE VALIDACIÓN:**
  1. Conector =><= obligatorio
  2. Verbo en tercera persona presente
  3. Objeto claro y específico
  4. Nudo canónico obligatorio
  5. [term] como cierre definitivo

**MODO DE PRÁCTICA:**
  • Modo normal: validación estándar
  • Modo estricto: validación rigurosa (comando: estricto)
  • Precisión >90%: listo para producción
  • Cristales STACKING: patrones consolidados
        """

    def _format_stats_response(self) -> str:
        """Respuesta de estadísticas soberanas."""
        try:
            from core.ledger import get_stats
            stats = get_stats()

            total = stats.get('transactions_total', 0)
            valid = stats.get('grammar_valid', 0)
            invalid = total - valid
            ratio = round((valid / total * 100), 1) if total > 0 else 0.0

            barra_total = 20
            barra_valid = int(barra_total * valid / total) if total > 0 else 0
            barra = "█" * barra_valid + "░" * (barra_total - barra_valid)

            lines = [
                "📊 **ESTADÍSTICAS SOBERANAS**",
                "",
                f"**Transacciones totales** : {total}",
                f"**VALID**                 : {valid}",
                f"**INVALID/otros**         : {invalid}",
                f"**Cristales STACKING**    : {stats.get('crystals_total', 0)}",
                "",
                f"**Precisión soberana**    : {ratio}%",
                f"  [{barra}] {ratio}%",
                "",
                f"  🔵 BLUE (KU no verificado) : {stats.get('blue_count', '—')}",
                f"  🟢 GREEN (WU cristalizado)  : {stats.get('green_count', '—')}",
                f"  🔤 UNICODE mode             : {stats.get('unicode_mode', 'STACKING')}",
                "",
                "Referencia:",
                "  < 40% — aprendiendo la forma",
                "  40-70% — forma consolidándose",
                "  > 70% — gramática soberana activa",
                "  > 90% — listo para escalar",
            ]
            
            # Mostrar cristales nuevos si aparecen
            if 'new_crystals' in stats:
                lines.append("")
                lines.append("✨ **Nuevos cristales STACKING**:")
                for c in stats['new_crystals']:
                    lines.append(f"  • {c}")
            
            return "\n".join(lines)
        except Exception as e:
            return f"❌ Error obteniendo estadísticas: {e}"

    def _format_status_response(self) -> str:
        """Respuesta de estado soberano."""
        coherence_ok = verify_coherence("chat")
        
        lines = [
            "🔧 **ESTADO SOBERANO ACTUAL**",
            f"**Chat State**: {self.state.value}",
            f"**Mensajes en sesión**: {len(self.session_history)}",
            f"**Coherencia [foundation]**: {'✅ OK' if coherence_ok else '❌ VIOLACIÓN'}",
        ]
        
        return "\n".join(lines)

    def process_message(self, user_input: str) -> ChatMessage:
        """
        Procesa un mensaje del usuario soberanamente.
        """
        start_time = time.time()
        self.state = ChatState.PROCESSING
        
        message = ChatMessage(user_input=user_input)
        
        try:
            # Verificar condiciones soberanas
            verify_sovereign_conditions("chat")
            
            # Comandos del sistema — tienen prioridad sobre traducción
            cmd = user_input.strip().lower()
            if cmd == "stats":
                message.response_type = ResponseType.VALIDATION
                message.response_content = self._format_stats_response()
                message.sovereign_verified = True
                message.processing_time_ms = int((time.time() - start_time) * 1000)
                self.session_history.append(message)
                self.state = ChatState.IDLE
                return message
            if cmd == "status":
                message.response_type = ResponseType.VALIDATION
                message.response_content = self._format_status_response()
                message.sovereign_verified = True
                message.processing_time_ms = int((time.time() - start_time) * 1000)
                self.session_history.append(message)
                self.state = ChatState.IDLE
                return message
            
            # Detectar tipo de input
            input_type = self._detect_input_type(user_input)
            
            if input_type == "help":
                message.response_type = ResponseType.HELP
                message.response_content = self._format_help_response()
                message.sovereign_verified = True
                
            elif input_type == "command":
                message.response_type = ResponseType.HELP
                cmd_lower = user_input.strip().lower()
                if cmd_lower in ("switch", "unicode"):
                    from core.ledger import switch_unicode, get_unicode_mode
                    mode = get_unicode_mode()
                    message.response_content = (
                        f"🔤 **UNICODE MODE ACTIVO**: {mode}\n"
                        f"Modos válidos: STACKING · LACHO · ASCII\n"
                        f"Para cambiar: switch STACKING / switch LACHO / switch ASCII"
                    )
                elif cmd_lower.startswith("switch "):
                    from core.ledger import switch_unicode
                    mode = cmd_lower.replace("switch ", "").strip().upper()
                    try:
                        result = switch_unicode(mode)
                        message.response_content = f"🔤 {result}"
                    except ValueError as e:
                        message.response_content = f"❌ {e}"
                elif cmd_lower in ("tomo", "tomos"):
                    from core.ledger import assign_tomo_ids
                    assigned = assign_tomo_ids()
                    lines = ["🔖 **TOMO_IDs ASIGNADOS**", ""]
                    for form, tomo in list(assigned.items())[:10]:
                        lines.append(f"  {tomo} → {form}")
                    if len(assigned) > 10:
                        lines.append(f"  ... y {len(assigned)-10} más")
                    message.response_content = "\n".join(lines)
                else:
                    message.response_content = f"Comando '{user_input}' procesado por el handler del sistema"
                message.sovereign_verified = True
                
            elif input_type == "natural":
                # Traducir a LACHO y validar
                self._last_translation_was_default = False
                lacho_sentence = self._translate_to_lacho(user_input)
                parsed = validate(lacho_sentence)
                
                # Registrar en ledger
                record_grammar(parsed)
                
                # Auditoría SAMU
                dispute = audit(parsed)
                if dispute:
                    message.response_type = ResponseType.DIRIMENCE
                    message.response_content = f"⚠️ **SAMU DETECTÓ DISPUTA**\n\n{dispute.description}\n\n**Traducción generada**:\n{lacho_sentence}"
                else:
                    if self._last_translation_was_default:
                        message.response_content = (
                            f"⚠️  **INPUT NO RECONOCIDO COMO PATRÓN LACHO**\n\n"
                            f"**Escribiste**: {user_input}\n"
                            f"**Sugerencia**: escribí directamente en gramática LACHO:\n"
                            f"  BIBLIOTECA Sujeto =><= .. verbo .. Objeto --[Nudo] [term]\n\n"
                            f"**O usá lenguaje natural conocido**:\n"
                            f"  verificar / iniciar / detener / dirimir / custodiar /\n"
                            f"  cristalizar / lanzar / proteger / autorizar\n\n"
                            f"**Traducción de emergencia generada** (para registro):\n"
                            f"{lacho_sentence}"
                        )
                    else:
                        message.response_type = ResponseType.VALIDATION
                        message.response_content = f"🔄 **TRADUCCIÓN + VALIDACIÓN**\n\n**Natural**: {user_input}\n\n**LACHO**: {lacho_sentence}\n\n{self._format_validation_response(parsed)}"
                
                message.sovereign_verified = True
                
            elif input_type == "lacho":
                # Validar directamente gramática LACHO
                parsed = validate(user_input)
                
                # Registrar en ledger
                record_grammar(parsed)
                
                # Auditoría SAMU
                dispute = audit(parsed)
                if dispute:
                    message.response_type = ResponseType.DIRIMENCE
                    message.response_content = f"⚠️ **SAMU DETECTÓ DISPUTA**\n\n{dispute.description}\n\n{self._format_validation_response(parsed)}"
                else:
                    message.response_type = ResponseType.VALIDATION
                    message.response_content = self._format_validation_response(parsed)
                
                message.sovereign_verified = True
                
            elif user_input.lower() == "stats":
                message.response_type = ResponseType.VALIDATION
                message.response_content = self._format_stats_response()
                message.sovereign_verified = True
                
            elif user_input.lower() == "status":
                message.response_type = ResponseType.VALIDATION
                message.response_content = self._format_status_response()
                message.sovereign_verified = True
                
            else:
                message.response_type = ResponseType.ERROR
                message.response_content = f"❌ No puedo procesar: {user_input}"
                message.sovereign_verified = False
            
            self.state = ChatState.IDLE
            
        except Exception as e:
            self.state = ChatState.ERROR
            message.response_type = ResponseType.ERROR
            message.response_content = f"❌ Error soberano: {e}"
            message.sovereign_verified = False
        
        # Calcular tiempo de procesamiento
        message.processing_time_ms = int((time.time() - start_time) * 1000)
        
        # Agregar al historial
        self.session_history.append(message)
        
        return message

    def get_session_summary(self) -> dict:
        """Resumen de la sesión actual."""
        total = len(self.session_history)
        if total == 0:
            return {"total": 0, "verified": 0, "errors": 0}
        
        verified = sum(1 for msg in self.session_history if msg.sovereign_verified)
        errors = sum(1 for msg in self.session_history if msg.response_type == ResponseType.ERROR)
        
        return {
            "total": total,
            "verified": verified,
            "errors": errors,
            "current_state": self.state.value,
        }


# ── Instancia global soberana ─────────────────────────────────────
_sovereign_chat = SovereignChat()

def ballpaper_render(state: dict) -> str:
    """
    BALLPAPER — superficie gráfica soberana · UNICODE estándar
    Muestra estado del sistema en tiempo real.
    Ref: BIBLIOTECAS_MADRE_LACHO · main.teather
    """
    score  = state.get("lacho_score", 0.0)
    scalar = state.get("scalar_s", 0.0)
    tx     = state.get("tx_total", 0)
    cristales = state.get("cristales", 0)
    
    # Indicadores UNICODE soberanos
    score_bar  = "●" * int(score * 10) + "○" * (10 - int(score * 10))
    scalar_bar = "●" * int(scalar * 10) + "○" * (10 - int(scalar * 10))
    
    return (
        f"╔══════════════════════════════╗\n"
        f"║  LACHO BALLPAPER — SOBERANO  ║\n"
        f"╠══════════════════════════════╣\n"
        f"║ SCORE  [{score_bar}] {score:.2f}  ║\n"
        f"║ SCALAR [{scalar_bar}] {scalar:.2f}  ║\n"
        f"║ TX: {tx:>6}  · CRISTALES: {cristales:>4} ║\n"
        f"╚══════════════════════════════╝"
    )


def ballpaper_render_notaria(acto: str, resultado_samu: str, scalar_s: float) -> str:
    """
    Render notarial soberano · extensión de ballpaper_render()
    Invoca desde: /api/notaria/certifica · /api/notaria/sella
    Scalar S threshold: 0.90 para H63 · 0.78 para WU
    """
    WIDTH = 46
    bar_len = 20
    filled = int(scalar_s * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)
    pct = int(scalar_s * 100)
    estado = "H63 既濟" if scalar_s >= 0.90 else "WU válido" if scalar_s >= 0.78 else "KU pendiente"
    nudo = "Nudo de Ocho" if scalar_s >= 0.90 else "As de Guía"
    
    lines = [
        "┌─ NOTARIA BALLPAPER " + "─" * (WIDTH - 20) + "┐",
        f"│ ACTO: {acto[:WIDTH-8]:<{WIDTH-8}} │",
        f"│ SAMU: {resultado_samu[:12]} · S={scalar_s:.2f} · {estado:<10} │",
        f"│ {bar} {pct}%{' ' * (WIDTH - bar_len - 6)} │",
        f"│ STACKING UF[H63] :: {nudo} [term]{' ' * (WIDTH - 37)} │",
        "└" + "─" * (WIDTH + 2) + "┘",
    ]
    return "\n".join(lines)


def chat(user_input: str) -> ChatMessage:
    """API pública soberana del chat."""
    return _sovereign_chat.process_message(user_input)

def get_summary() -> dict:
    """API pública soberana de resumen de sesión."""
    return _sovereign_chat.get_session_summary()


# ── Test soberano de arranque ─────────────────────────────────────
if __name__ == "__main__":
    print("═" * 60)
    print("DIRIME IMV — Chat AI Soberano")
    print("═" * 60)
    
    test_inputs = [
        "help",
        "verificar el sistema",
        "TRUST FOUNDATION =><= .. verifica .. scope_activo --[As de Guía] [term]",
        "stats",
        "status",
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 Usuario: {user_input}")
        message = chat(user_input)
        print(f"⏱️  Tiempo: {message.processing_time_ms}ms")
        print(f"✅ Verificado: {message.sovereign_verified}")
        print(f"🤖 Respuesta:\n{message.response_content}")
        print("-" * 40)
    
    summary = get_summary()
    print(f"\n📊 Resumen de sesión: {summary}")
    print("═" * 60)

# Test inmediato — ejecutar tras guardar:
if __name__ == "__main__":
    # Test original
    print("═" * 60)
    print("DIRIME IMV — Chat AI Soberano")
    print("═" * 60)
    
    test_inputs = [
        "help",
        "verificar el sistema",
        "TRUST FOUNDATION =><= .. verifica .. scope_activo --[As de Guía] [term]",
        "stats",
        "status",
    ]
    
    for user_input in test_inputs:
        print(f"\n👤 Usuario: {user_input}")
        message = chat(user_input)
        print(f"⏱️  Tiempo: {message.processing_time_ms}ms")
        print(f"✅ Verificado: {message.sovereign_verified}")
        print(f"🤖 Respuesta:\n{message.response_content}")
        print("-" * 40)
    
    # Test ballpaper_render_notaria
    print("\n" + "=" * 50)
    print("TEST NOTARIA BALLPAPER RENDER")
    print("=" * 50)
    print(ballpaper_render_notaria(
        acto="certifica documento_X",
        resultado_samu="VALID",
        scalar_s=0.92
    ))
    print("=" * 50)
