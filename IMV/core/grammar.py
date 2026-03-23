"""
DIRIME IMV — grammar.py
Validador soberano de sentencias en gramática viva LACHO.

Sentencia canónica:
  [Biblioteca] Sujeto =><= .. verbo .. Objeto --[Nudo] [term]

Referencia canónica:
  BIBLIO-SOURCES(GRAMATICA VIVA).txt

--- LACHO FORMAL GRAMMAR — BNF CONTRACT v1.0 ---
Context-sensitive (Chomsky N3) — maps to LACHO sentence structure

SENTENCE    ::= LIBRARY SUBJECT BIND VERB OBJECT NUDO TERM
LIBRARY     ::= "TRUST" | "SAMU" | "CRYPTO" | "GATE" | "STACKING"
              | "WORK" | "SOCIAL" | "METHOD" | "ACTIVITY" | "COGNITIVO"
BIND        ::= "=><=">
NUDO        ::= "--[" NUDO_TYPE "]"
NUDO_TYPE   ::= "As de Guía" | "Ballestrinque" | "⊗" | "Corredizo"
TERM        ::= "[" IDENTIFIER "]"
ABORT       ::= "!!" "Abort" "!!" ("--" "--" IDENTIFIER)?
CONV_DEF    ::= IDENTIFIER "::=" EXPRESSION

SLOTS: exactly 6 mandatory positions before TERM
DEPTH_MAX: 64 (maps to 64 UF hexagrams)
ENCODING: UTF-8, CJK block U+4E00-U+9FFF supported
[TASK_1.1 BNF CONTRACT v1.0]
"""

from __future__ import annotations
import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List, Tuple, Union

# Import taxonomy for notarial classification
from .taxonomy import TaxonomyLACHO, classify_scalar, is_notaria_allowed, is_certifica_allowed

from .foundation import (
    SovereignError,
    verify_sovereign_conditions,
)

MAX_RECURSION_DEPTH = 64  # maps to 64 UF hexagrams — TASK_1.2

def is_chinese(text: str) -> bool:
    """Detecta si el texto contiene caracteres CJK soberanos."""
    return any('\u4e00' <= c <= '\u9fff' or '\u3400' <= c <= '\u4dbf' for c in text)

CJK_TOKEN_MAP = {
    "信任": ("TRUST", "FOUNDATION",     "H01", +0.05),
    "关系": ("SOCIAL", "{relay}",       "H08", +0.05),
    "面子": ("SAMU",   "@",             "H15", +0.05),
    "资本": ("STACKING","UF[H48]",      "H48", +0.05),
    "交易": ("WORK",   "{actuator}",    "H49", +0.05),
    "合同": ("TRUST",  "[term]",        "H43", +0.05),
    "安全": ("CRYPTO", "(shield seat)", "H14", +0.05),
    "验证": ("TRUST",  "FOUNDATION",    "H61", +0.05),
    "数字": ("CRYPTO", "(spark seat)",  "H30", +0.05),
    "货币": ("CRYPTO", "(flow seat)",   "H58", +0.05),
    "银行": ("SOCIAL", "{launch-bot}",  "H07", +0.05),
    "贷款": ("METHOD", "<equation>",    "H42", +0.05),
    "风险": ("GATE",   "UF[H06]",       "H06", +0.05),
    "网络": ("STACKING","UF[H52]",      "H52", +0.05),
    "节点": ("ACTIVITY","UF[H57]",      "H57", +0.05),
    "主权": ("TRUST",  "[scope]",       "H01", +0.05),
    "协议": ("TRUST",  "[management]",  "H60", +0.05),
    "社区": ("SOCIAL", "{chair}",       "H13", +0.05),
    "智能": ("METHOD", "<operator_flow>","H50",+0.05),
    "桥梁": ("WORK",   "{actuator}",    "H59", +0.05),
}

def resolve_chinese_token(zh: str) -> dict:
    """Resuelve un ideograma CJK a su token LACHO canónico."""
    entry = CJK_TOKEN_MAP.get(zh)
    if not entry:
        return {"found": False, "zh": zh}
    lib, subject, hexagram, bonus = entry
    return {
        "found": True, "zh": zh,
        "library": lib, "subject": subject,
        "hexagram": hexagram, "score_bonus": bonus,
        "unicode_mode": "CHINA"
    }

TAXONOMY_MAP = {
    "COGNITIVO":  {"level": 0, "scalar_min": 0.95, "class": "constitucional"},
    "TRUST":      {"level": 1, "scalar_min": 0.88, "class": "biblioteca"},
    "SAMU":       {"level": 1, "scalar_min": 0.88, "class": "biblioteca"},
    "CRYPTO":     {"level": 1, "scalar_min": 0.88, "class": "biblioteca"},
    "GATE":       {"level": 1, "scalar_min": 0.88, "class": "biblioteca"},
    "ACTIVITY":   {"level": 1, "scalar_min": 0.88, "class": "biblioteca"},
    "WORK":       {"level": 1, "scalar_min": 0.88, "class": "biblioteca"},
    "STACKING":   {"level": 1, "scalar_min": 0.88, "class": "biblioteca"},
    "SOCIAL":     {"level": 1, "scalar_min": 0.88, "class": "biblioteca"},
    "METHOD":     {"level": 1, "scalar_min": 0.88, "class": "biblioteca"},
    "THEATER":    {"level": 2, "scalar_min": 0.85, "class": "modulo"},
    "RUNNER":     {"level": 2, "scalar_min": 0.85, "class": "modulo"},
    "KALIL":      {"level": 2, "scalar_min": 0.85, "class": "modulo"},
    "ELPULSAR":   {"level": 2, "scalar_min": 0.85, "class": "modulo"},
}

def classify_sentence(parsed) -> dict:
    """Clasifica sentencia en jerarquía TAXONOMY_LACHO."""
    lib = parsed.library.value if hasattr(parsed.library, 'value') else str(parsed.library)
    tax = TAXONOMY_MAP.get(lib, {"level": 3, "scalar_min": 0.80, "class": "operador"})
    errors = getattr(parsed, 'errors', [])
    warnings = getattr(parsed, 'warnings', [])
    score = 0.0
    if not errors:
        score = 0.5
        if getattr(parsed, 'verb', '') in VERBOS_CANONICOS_LACHO:
            score += 0.1
        if not any("sujeto" in w.lower() for w in warnings):
            score += 0.1
        if getattr(parsed, 'knot', '') in {
            "As de Guía","Nudo de Ocho","Ballestrinque",
            "Nudo Corredizo","Nudo de Rizo"}:
            score += 0.1
        if not warnings:
            score += 0.1
        if getattr(parsed, 'unicode_mode', 'STANDARD') == 'CHINA':
            score += 0.05
    return {
        "taxonomy_level": tax["level"],
        "taxonomy_class": tax["class"],
        "scalar_min": tax["scalar_min"],
        "meets_threshold": round(score, 3) >= tax["scalar_min"]
    }


# ── Enums soberanos ───────────────────────────────────────────────
class Library(Enum):
    TRUST    = "TRUST"
    SOCIAL   = "SOCIAL"
    CRYPTO   = "CRYPTO"
    ACTIVITY = "ACTIVITY"
    METHOD   = "METHOD"
    SAMU     = "SAMU"
    WORK     = "WORK"
    STACKING = "STACKING"
    GATE     = "GATE"
    UNKNOWN  = "UNKNOWN"


class Knot(Enum):
    """Nudos soberanos canónicos de LACHO."""
    AS_DE_GUIA      = "As de Guía"
    NUDO_DE_OCHO    = "Nudo de Ocho"
    BALLESTRINQUE   = "Ballestrinque"
    NUDO_CORREDIZO  = "Nudo Corredizo"
    NUDO_DE_RIZO    = "Nudo de Rizo"
    UNKNOWN         = "UNKNOWN"


class ValidationResult(Enum):
    VALID   = "VALID"
    INVALID = "INVALID"
    WARNING = "WARNING"


# ── Delimitadores por biblioteca ──────────────────────────────────
LIBRARY_DELIMITERS = {
    Library.TRUST:    (r"\[", r"\]"),
    Library.SOCIAL:   (r"\{", r"\}"),
    Library.CRYPTO:   (r"\(", r"\)"),
    Library.ACTIVITY: (r"!!", r"!!"),
    Library.METHOD:   (r"<", r">"),
}

# Patrones de nudos aceptados
KNOT_PATTERNS = [
    r"As de Guía",
    r"Nudo de Ocho",
    r"Ballestrinque",
    r"Nudo Corredizo",
    r"Nudo de Rizo",
]

# Patrón del conector soberano
SUBJECT_CONNECTOR = r"=><=\s*\.\.\s*"  # =><= .. verbo ..


# ── Sistema KEYWORDS — Estados transversales del kernel ──────────────────────────────────
KEYWORDS_SYSTEM = {
    "COGNITIVE_RAG":      "recuperación semántica — Journal",
    "BEHAVIORAL_RAG":     "patrones de conducta — ledger soberano",
    "BLUE_WORDS":         "constantes inmutables ReadOnly",
    "GREEN_KNOWLEDGE":    "filtro de valor verificado delta-Ψ > 0",
    "RED_REGRET":         "rollback ante fallo crítico — H06",
    "HYPERLEDGER_FABRIC": "ledger distribuido inmutable",
    "BIOMETRICS":         "validación física de identidad — key seat",
    "DOORMAN_MOBILE":     "perímetro móvil de acceso soberano",
}

# Los Keywords son estados transversales del kernel.
# No tienen delimitador gramatical propio.
# Se activan por nombre en el Journal operacional.
# El sistema los consulta antes de cada ciclo de instrucción Ψ.


# ── Modelo de sentencia parseada ──────────────────────────────────
# ── Paradigmas por biblioteca — validación diferenciada ──────────
# Referencia: BIBLIO-SOURCES(DIRIME-IMV_PARADIGM).txt
PARADIGM_RULES = {
    "TRUST": {
        "mode": "imperativo",
        "valid_modules": [
            "foundation","scope","term","command","scenario",
            "event","element","ecosystem","management","language",
            "what","when","how","ku-chat","wu-mail","mu-store",
            "rabbit-faith","logistical-executive"
        ],
        "note": "declaración directa — módulos entre [ ]"
    },
    "SOCIAL": {
        "mode": "declarativo",
        "forbidden_verbs": ["ignite","commit","purge","destruye","elimina"],
        "valid_modules": [
            "chair","scheduler","drip","headcat","masking",
            "streaming","launch-bot","note","concierge-desk",
            "guest-services","handshake","relay","rocking-chair",
            "scheduler-os","dogma-virtual"
        ],
        "note": "describe estado relacional — módulos entre { }"
    },
    "CRYPTO": {
        "mode": "funcional",
        "valid_subjects": [
            "direction seat","key seat","ignition seat","shield seat",
            "flow seat","link seat","spark seat","head seat",
            "way agnostic atheism","seal of secrecy"
        ],
        "note": "asientos de autoridad — módulos entre ( )"
    },
    "WORK": {
        "mode": "bajo nivel",
        "valid_modules": [
            "actuator","brake","doorman-mobile","door-afternoon",
            "masking-folder","green-knowledge","data-center"
        ],
        "valid_hexagrams": ["H52","H06"],
        "note": "ejecución física — H52 quietud + H06 conflicto"
    },
    "GATE": {
        "mode": "script",
        "canonical_hexagrams": ["H03", "H05", "H56", "H06"],
        "sequence_logic": "H03→H05→H56→H06",
        "note": "H03=inicio·dificultad · H05=espera · H56=tránsito · H06=conflicto/resolución"
    },
    "METHOD": {
        "mode": "enumerable",
        "valid_operators": [
            "<equation>","<if>","<operator_flow>",
            "<stat_onto>","<psi_spin>"
        ],
        "note": "operadores formales entre < >"
    },
    "ACTIVITY": {
        "mode": "nivel medio",
        "requires_uf": True,
        "note": "sujeto UF[H##] — rango H01-H64"
    },
    "SAMU": {
        "mode": "alto nivel",
        "valid_subjects": [
            "@","@trust_matrix","@human_early","@human_later",
            "#rise","#set",
            "$mon","$tue","$wed","$thu","$fri","$sat","$sun"
        ],
        "note": "operadores canónicos SAMU"
    },
    "STACKING": {
        "mode": "orientado a objetos",
        "familia_real": ["H01","H02","H29","H30","H51","H52","H57","H58"],
        "extensiones": ["H04","H23","H48","H63"],
        "note": "familia real I Ching BASE/CENTER/TOP + extensiones"
    },
}


# ── Verbos naturales por biblioteca ───────────────────────────────
# Referencia: GUÍA DIRIME IMV — Referencia rápida
VERBOS_NATURALES = {
    "TRUST":    ["verifica", "declara", "sostiene", "autoriza", "limita"],
    "WORK":     ["materializa", "ejecuta", "detiene", "custodia", "sella", "{flybot}", "{doorman-mobile}", "{actuator}", "{green-knowledge}", "{masking-folder}"],
    "SAMU":     ["dirime", "audita", "modera", "registra", "activa"],
    "ACTIVITY": ["inicia", "aquieta", "penetra", "cristaliza", "lanza"],
    "CRYPTO":   ["autoriza", "certifica", "protege", "firma", "conecta"],
    "SOCIAL":   ["lanza", "recibe", "filtra", "distribuye", "registra"],
    "GATE":     ["suspende", "transita", "resuelve", "filtra", "permite", "espera"],
    "STACKING": ["cristaliza", "inmutabiliza", "preserva", "archiva", "sella"],
    "METHOD":   ["define", "formaliza", "opera", "calcula", "estructura"],
}


# ── Sujetos canónicos por biblioteca ──────────────────────────────
SUJETOS_CANONICOS = {
    "TRUST":    ["FOUNDATION", "[scope]", "[term]", "[command]", "[foundation]"],
    "WORK":     ["{actuator}", "{brake}", "{doorman-mobile}", "{door-afternoon}"],
    "SAMU":     ["@", "#rise", "#set", "$mon", "$tue", "$wed", "$thu", "$fri", "$sat", "$sun", "@trust_matrix"],
    "ACTIVITY": ["UF[H01]", "UF[H03]", "UF[H05]", "UF[H52]", "UF[H56]", "UF[H57]", "UF[H63]", "UF[H64]", "UF[H06]"],
    "CRYPTO":   ["(spark seat)", "(shield seat)", "(key seat)", "(link seat)"],
    "SOCIAL":   ["{chair}", "{drip}", "{launch-bot}", "{masking}", "{tether}", "{scheduler}", "{relay}", "{headcat}", "{concierge-desk}", "{rocking-chair}", "{streaming}", "{handshake}", "{guest-services}"],
    "GATE":     ["UF[H03]", "UF[H05]", "UF[H56]", "UF[H06]"],
    "STACKING": ["UF[H52]", "UF[H01]", "UF[H48]", "UF[H63]"],
    "METHOD":   ["<equation>", "<operator_flow>", "<if>", "<loop>", "<stat_onto>"],
}
# NOTARIA GÉNESIS · $thu 2026-03-12 · H63 既濟
# acto_notarial: objeto válido CRYPTO·STACKING·TRUST
# UF[H63]: STACKING inmutabiliza acto cerrado

# ── PARADIGM_RULES ─────────────────────────────────────────────────────
# Reglas de validación por paradigma de biblioteca
# Referencia: BIBLIO-SOURCES(GAP_PARADIGMAS_GRAMMAR).txt
PARADIGM_RULES = {
    "TRUST":    {"mode": "imperativo",  "valid_modules": ["foundation","scope","term","command","scenario","event","element","ecosystem","management","language","what","when","how","ku-chat","wu-mail","mu-store","rabbit-faith"]},
    "SOCIAL":   {"mode": "declarativo", "forbidden_verbs": ["ignite","commit","purge","destruye","elimina"]},
    "CRYPTO":   {"mode": "funcional",   "requires_seat_subject": True, "valid_subjects": ["(spark seat)","(shield seat)","(key seat)","(link seat)","(direction seat)","(flow seat)","(seal of secrecy)"]},
    "GATE":     {"mode": "script",      "valid_hexagrams": ["H03","H05","H56","H06"]},
    "WORK":     {"mode": "bajo_nivel",  "valid_subjects": ["{actuator}","{brake}","{doorman-mobile}","{door-afternoon}","{green-knowledge}","{masking-folder}"]},
    "METHOD":   {"mode": "enumerable",  "valid_operators": ["<equation>","<operator_flow>","<if>","<stat_onto>","<loop>"]},
    "ACTIVITY": {"mode": "intermedio",  "active_slots": ["UF[H01]","UF[H02]","UF[H03]","UF[H05]","UF[H06]","UF[H24]","UF[H29]","UF[H30]","UF[H42]","UF[H48]","UF[H49]","UF[H51]","UF[H52]","UF[H56]","UF[H57]","UF[H58]","UF[H63]","UF[H64]"]},
    "SAMU":     {"mode": "alto_nivel",  "valid_subjects": ["@","@trust_matrix","#rise","#set","$mon","$tue","$wed","$thu","$fri","$sat","$sun"]},
    "STACKING": {"mode": "orientado_objetos", "valid_subjects": ["UF[H01]","UF[H02]","UF[H04]","UF[H23]","UF[H29]","UF[H30]","UF[H48]","UF[H51]","UF[H52]","UF[H57]","UF[H58]"]},
}

@dataclass
class ParsedSentence:
    raw: str
    library: Library = Library.UNKNOWN
    subject: str = ""
    verb: str = ""
    obj: str = ""
    knot: str = ""
    term_present: bool = False
    unicode_mode: str = "STANDARD"   # STANDARD | CHINA
    cjk_tokens: list = field(default_factory=list)
    taxonomy: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def result(self) -> ValidationResult:
        if self.errors:
            return ValidationResult.INVALID
        if self.warnings:
            return ValidationResult.WARNING
        return ValidationResult.VALID

    def summary(self) -> str:
        lines = [
            f"  raw: {self.raw}",
            f"  library: {self.library.value}",
            f"  subject: {self.subject}",
            f"  verb: {self.verb}",
            f"  obj: {self.obj}",
            f"  knot: {self.knot}",
            f"  [term]    : {'presente' if self.term_present else 'AUSENTE'}",
        ]
        if self.errors:
            lines.append(f"  errores   : {' | '.join(self.errors)}")
        if self.warnings:
            lines.append(f"  avisos    : {' | '.join(self.warnings)}")
        if self.unicode_mode == "CHINA":
            zh_list = [t['zh'] for t in self.cjk_tokens]
            lines.append(f"  unicode_mode: CHINA · tokens: {' '.join(zh_list)}")
        if self.taxonomy:
            t = self.taxonomy
            mark = "✅" if t.get('meets_threshold') else "⚠"
            lines.append(f"  taxonomy  : N{t['taxonomy_level']}·{t['taxonomy_class']} · min={t['scalar_min']} {mark}")
        return "\n".join(lines)


# ── Validador soberano ────────────────────────────────────────────
# Tabla de normalización de verbos comunes
VERB_NORMALIZATIONS = {
    "verificar":     "verifica",
    "validar":       "valida",
    "iniciar":       "inicia",
    "declarar":      "declara",
    "registrar":     "registra",
    "evaluar":       "evalúa",
    "penetrar":      "penetra",
    "conectar":      "conecta",
    "bloquear":      "bloquea",
    "cerrar":        "cierra",
    "procesar":      "procesa",
    "transitar":     "transita",
    "transito":      "transita",   # sustantivo usado como verbo
    "suspender":     "suspende",
    "esperar":       "espera",
    "conflicto":     "conflictúa", # sustantivo — WARNING especial
    "resolver":      "resuelve",
    "monitorear":    "monitorea",
    "aprender":      "aprende",
    "fluir":         "fluye",
    "invertir":      "invierte",
}

def normalize_verb(verb: str) -> tuple[str, bool]:
    verb_lower = verb.lower().strip()
    if verb_lower in VERB_NORMALIZATIONS:
        return VERB_NORMALIZATIONS[verb_lower], True
    if verb_lower.endswith("ar") and len(verb_lower) > 3:
        normalized = verb_lower[:-2] + "a"
        return normalized, True
    return verb, False



# ── GATE SEQUENCE NOTARIAL ───────────────────────────────────────
def gate_sequence_notaria(state: str) -> str:
    """Mapea secuencia de estados GATE para flujo notarial.
    
    Secuencia notarial:
    H03 → H05  (espera partes)
    H05 → H56  (contiene → viajero=acto)
    H56 → H06  (acto en tránsito → conflicto resuelto)
    H06 → H63  (resolución → consumación notarial)
    """
    sequence_map = {
        "H03": "H05",  # espera partes
        "H05": "H56",  # contiene → viajero=acto
        "H56": "H06",  # acto en tránsito → conflicto resuelto
        "H06": "H63",  # resolución → consumación notarial
        "H63": "H63",  # estado final notarial
    }
    return sequence_map.get(state, state)


# SCHEDULER-OS (SOCIAL_SCHEDULER-OS): estados H1→H5→H56→H6
# {scheduler} opera como OS soberano con ciclos de latencia
# H1=Génesis·activo H5=Espera·latente H56=Tránsito·en_curso H6=Conflicto·bloqueado
class GrammarValidator:
    """
    Valida sentencias en gramática viva LACHO.
    Referencia: BIBLIO-SOURCES(GRAMATICA VIVA).txt

    Reglas soberanas verificadas:
      1. Debe contener =><= como conector soberano.
      2. Debe contener .. verbo .. como acción declarada.
      3. Debe cerrar con --[Nudo] [term].
      4. El nudo debe ser uno de los nudos canónicos.
      5. [term] es obligatorio — sin cierre no hay ciclo válido.
      
    Actualización corpus:
      - KEYWORDS_SYSTEM agregado como referencia transversal
      - VALID_TRUST_MODULES actualizado con [logistical-executive]
    """

    def __init__(self):
        # Referencia a KEYWORDS_SYSTEM del módulo
        self.KEYWORDS_SYSTEM = {
            "COGNITIVE_RAG":      "recuperación semántica — Journal",
            "BEHAVIORAL_RAG":     "patrones de conducta — ledger soberano",
            "BLUE_WORDS":         "constantes inmutables ReadOnly",
            "GREEN_KNOWLEDGE":    "filtro de valor verificado delta-Ψ > 0",
            "RED_REGRET":         "rollback ante fallo crítico — H06",
            "HYPERLEDGER_FABRIC": "ledger distribuido inmutable",
            "BIOMETRICS":         "validación física de identidad — key seat",
            "DOORMAN_MOBILE":     "perímetro móvil de acceso soberano",
        }
        
        # Módulos TRUST válidos según corpus verificado
        self.VALID_TRUST_MODULES = [
            "foundation","scope","term","command","scenario",
            "event","element","ecosystem","management","language",
            "what","when","how","ku-chat","wu-mail","mu-store",
            "rabbit-faith","logistical-executive"
        ]
        
        # Regex compilados una sola vez
        self._re_verb    = re.compile(r'=><= *\.\. *(.+?) *\.\.')
        self._re_knot    = re.compile(r'--\[([^\]]+)\]')
        self._re_term    = re.compile(r'\[term\]', re.IGNORECASE)
        self._re_subject_crypto = re.compile(r'(\([^)]+\))\s*=><=')
        self._re_subject_work   = re.compile(r'(\{[^}]+\})\s*=><=')
        self._re_subject_uf     = re.compile(r'(UF\[H\d+\])\s*=><=')
        self._re_subject_samu   = re.compile(r'([@#\$][\w\-]*)\s*=><=')
        self._re_subject_trust  = re.compile(
            r'((?:FOUNDATION|'
            r'\[(?:foundation|scope|term|command|scenario|event|element|'
            r'ecosystem|management|language|what|when|how|'
            r'ku-chat|wu-mail|mu-store|rabbit-faith|logistical-executive)'
            r'\]))\s*=><=',
            re.IGNORECASE
        )
        self._re_subject_method = re.compile(r'(<[^>]+>)\s*=><=')

    # ── Reglas de validación ──────────────────────────────────────
    def _check_connector(self, sentence: str, parsed: ParsedSentence) -> None:
        """Regla 1: =><= debe estar presente."""
        if "=><=".strip() not in sentence:
            parsed.errors.append("Conector soberano '=><=' ausente.")

    def _check_verb(
        self, sentence: str, parsed: ParsedSentence
    ) -> None:
        """Regla 2: .. verbo .. debe estar presente y canónico."""
        verb_pattern = self._re_verb.search(sentence)
        if verb_pattern:
            raw_verb = verb_pattern.group(1).strip()
            normalized, was_normalized = normalize_verb(raw_verb)
            parsed.verb = normalized
            if was_normalized and raw_verb != normalized:
                warning_msg = f"Verbo normalizado: '{raw_verb}' → '{normalized}' (forma canónica LACHO)"
                # WARNING especial para "conflicto"
                if raw_verb.lower() == "conflicto":
                    warning_msg += " | conflicto es sustantivo — forma verbal: conflictúa o usar verbo descriptivo"
                parsed.warnings.append(warning_msg)
        else:
            parsed.errors.append(
                "Estructura de verbo '.. verbo ..' ausente."
            )

    def _warn_verb_mismatch(self, parsed: ParsedSentence) -> None:
        """
        Advertencia: verbo no pertenece al conjunto natural de la biblioteca.
        No invalida la sentencia — agrega WARNING soberano.
        """
        lib = parsed.library.value
        if not parsed.verb or lib not in VERBOS_NATURALES:
            return
        naturales = [v.lower() for v in VERBOS_NATURALES.get(lib, [])]
        if parsed.verb.lower() not in naturales:
            parsed.warnings.append(
                f"Verbo '{parsed.verb}' no natural para biblioteca {lib}. "
                f"Verbos naturales: {', '.join(VERBOS_NATURALES[lib])}."
            )

    def _warn_subject_mismatch(self, parsed: ParsedSentence) -> None:
        """
        Advertencia: sujeto no pertenece al conjunto canónico de la biblioteca.
        No invalida la sentencia — agrega WARNING soberano.
        """
        lib = parsed.library.value
        subj = parsed.subject
        if not subj or lib not in SUJETOS_CANONICOS:
            return
        canonicos = SUJETOS_CANONICOS.get(lib, [])
        if subj not in canonicos:
            parsed.warnings.append(
                f"Sujeto '{subj}' no canónico para biblioteca {lib}. "
                f"Sujetos canónicos: {', '.join(canonicos)}."
            )

    def _check_knot_and_term(self, sentence: str, parsed: ParsedSentence) -> None:
        """Regla 3+4+5: --[Nudo] y [term] obligatorios."""
        # Detectar -- [Nudo] con espacio — error frecuente
        spaced_knot = re.search(r'--\s+\[', sentence)
        if spaced_knot:
            parsed.warnings.append(
                "Espacio entre '--' y '[Nudo]' detectado. "
                "Forma correcta: --[Nudo] sin espacio."
            )
        
        # Buscar --[Nudo]
        knot_match = self._re_knot.search(sentence)
        if knot_match:
            knot_text = knot_match.group(1)
            CANONICAL_EXACT = [
                "As de Guía",
                "Nudo de Ocho",
                "Ballestrinque",
                "Nudo Corredizo",
                "Nudo de Rizo",
            ]
            CANONICAL_CASE = [
                "as de guía",
                "nudo de ocho",
                "ballestrinque",
                "nudo corredizo",
                "nudo de rizo",
            ]
            # Verificar si es canónico exacto
            if knot_text in CANONICAL_EXACT:
                parsed.knot = knot_text
            elif knot_text.lower() in CANONICAL_CASE:
                parsed.warnings.append(
                    f"Nudo '{knot_text}' reconocido pero no canónico. "
                    f"Forma exacta requerida: mayúsculas y tildes. "
                    f"Nudos válidos: {', '.join(CANONICAL_EXACT)}"
                )
                parsed.knot = knot_text
            else:
                parsed.errors.append(
                    f"Nudo '{knot_text}' no es canónico. "
                    f"Nudos válidos: {', '.join(CANONICAL_EXACT)}"
                )
                parsed.knot = knot_text
        else:
            parsed.errors.append("Nudo soberano '--[Nudo]' ausente.")

        # Verificar [term]
        # Buscar el ÚLTIMO [term] — no el primero.
        # TRUST [term] como módulo sujeto genera falso positivo
        # si se busca el primero. El cierre soberano es siempre el último.
        all_terms = list(self._re_term.finditer(sentence))
        term_match = all_terms[-1] if all_terms else None

        if term_match:
            parsed.term_present = True
            after_term = sentence[term_match.end():].strip()
            after_term_clean = re.sub(r'^[\s\.]+$', '', after_term)
            if after_term_clean:
                parsed.warnings.append(
                    f"Contenido después de [term]: "
                    f"'{after_term_clean[:30]}' "
                    f"— [term] debe ser el cierre definitivo."
                )
        else:
            parsed.errors.append(
                "[term] ausente — sin cierre no hay ciclo soberano válido."
            )

    def _check_delimiter_consistency(
        self, sentence: str, parsed: ParsedSentence
    ) -> None:
        """
        Valida reglas de paradigma por biblioteca.
        Genera WARNING — no INVALID.
        El sistema avisa sin bloquear.
        Referencia: BIBLIO-SOURCES(DIRIME-IMV_PARADIGM).txt
        """
        lib = parsed.library.value
        rules = PARADIGM_RULES.get(lib)
        if not rules:
            return

        # SOCIAL: verbos prohibidos
        if lib == "SOCIAL" and parsed.verb:
            forbidden = rules.get("forbidden_verbs", [])
            if parsed.verb.lower() in forbidden:
                parsed.warnings.append(
                    f"Paradigma SOCIAL (declarativo): "
                    f"verbo '{parsed.verb}' es de ejecución directa. "
                    f"SOCIAL describe estado — verbos válidos: "
                    f"lanza, distribuye, filtra, modera, recibe."
                )

        # CRYPTO: sujeto debe ser asiento canónico
        if lib == "CRYPTO" and parsed.subject:
            valid_seats = rules.get("valid_subjects", [])
            subj_lower = parsed.subject.lower().strip("()")
            is_seat = any(s in subj_lower for s in valid_seats)
            if not is_seat:
                parsed.warnings.append(
                    f"Paradigma CRYPTO (funcional): "
                    f"'{parsed.subject}' no es asiento de autoridad. "
                    f"Válidos: (spark seat) (shield seat) (key seat) "
                    f"(link seat) (flow seat) (head seat) etc."
                )

        # GATE: hexagrama canónico
        if lib == "GATE" and parsed.subject:
            canonical = rules.get("canonical_hexagrams", [])
            has_canonical = any(h in parsed.subject for h in canonical)
            if "UF[" in parsed.subject and not has_canonical:
                parsed.warnings.append(
                    f"Paradigma GATE (script): "
                    f"'{parsed.subject}' no es hexagrama canónico GATE. "
                    f"Canónicos: UF[H05] espera · UF[H56] tránsito · UF[H06] conflicto."
                )

        # METHOD: operador del set canónico
        if lib == "METHOD" and parsed.subject:
            valid_ops = rules.get("valid_operators", [])
            if parsed.subject and parsed.subject not in valid_ops:
                parsed.warnings.append(
                    f"Paradigma METHOD (enumerable): "
                    f"'{parsed.subject}' no está en el set canónico. "
                    f"Válidos: {', '.join(valid_ops)}"
                )

        # ACTIVITY y STACKING: requieren UF[H##]
        if lib in ("ACTIVITY", "STACKING") and parsed.subject:
            if parsed.subject and "UF[H" not in parsed.subject:
                parsed.warnings.append(
                    f"Paradigma {lib}: sujeto '{parsed.subject}' "
                    f"debería ser UF[H##]. Rango H01-H64."
                )

        # STACKING: verificar familia real + extensiones
        if lib == "STACKING" and parsed.subject and "UF[H" in parsed.subject:
            familia = rules.get("familia_real", [])
            extensiones = rules.get("extensiones", [])
            valid_uf = familia + extensiones
            h_match = re.search(r'UF\[H(\d+)\]', parsed.subject)
            if h_match:
                h_num = f"H{int(h_match.group(1)):02d}"
                if h_num not in valid_uf:
                    parsed.warnings.append(
                        f"Paradigma STACKING: UF[{h_num}] no está en "
                        f"la familia verificada. "
                        f"Familia real: H01 H02 H29 H30 H51 H52 H57 H58. "
                        f"Extensiones: H04 H23 H48. "
                        f"Revisa la documentación para más detalles."
                    )

        # SAMU: sujeto canónico
        if lib == "SAMU" and parsed.subject:
            valid_subs = rules.get("valid_subjects", [])
            if parsed.subject and parsed.subject not in valid_subs:
                parsed.warnings.append(
                    f"Paradigma SAMU (alto nivel): "
                    f"'{parsed.subject}' no es operador canónico. "
                    f"Válidos: @ @trust_matrix @human_early @human_later "
                    f"#rise #set $mon $tue $wed $thu $fri $sat $sun"
                )

    def _validate_by_paradigm(
        self, sentence: str, parsed: ParsedSentence
    ) -> None:
        """
        Valida reglas de paradigma por biblioteca según PARADIGM_RULES.
        Genera WARNING — no INVALID.
        Referencia: BIBLIO-SOURCES(GAP_PARADIGMAS_GRAMMAR).txt
        """
        lib = parsed.library.value if hasattr(parsed.library,'value') else str(parsed.library)
        rules = PARADIGM_RULES.get(lib, {})
        
        # SOCIAL: verbos prohibidos
        if rules.get("forbidden_verbs") and parsed.verb and parsed.verb.lower() in rules["forbidden_verbs"]:
            parsed.warnings.append(f"Verbo '{parsed.verb}' prohibido en paradigma {rules['mode']} ({lib})")
        
        # CRYPTO: requiere sujeto (seat)
        if rules.get("requires_seat_subject"):
            if parsed.subject and not any(s in parsed.subject for s in rules.get("valid_subjects",[])):
                parsed.warnings.append(f"CRYPTO funcional requiere sujeto (seat) — recibido: '{parsed.subject}'")
        
        # GATE: hexagrama válido
        if rules.get("valid_hexagrams"):
            if parsed.subject and not any(h in parsed.subject for h in rules["valid_hexagrams"]):
                parsed.warnings.append(f"GATE requiere hexagrama en {rules['valid_hexagrams']}")
        
        # METHOD: operador válido
        if lib == "METHOD" and rules.get("valid_operators"):
            if parsed.subject and not any(op in parsed.subject for op in rules["valid_operators"]):
                parsed.warnings.append(f"METHOD enumerable requiere operador del set")

        # ACTIVITY y STACKING: requieren UF[H##]
        if lib in ("ACTIVITY", "STACKING") and parsed.subject:
            if parsed.subject and "UF[H" not in parsed.subject:
                parsed.warnings.append(
                    f"Paradigma {lib}: sujeto '{parsed.subject}' "
                    f"debería ser UF[H##]. Rango H01-H64."
                )

        # STACKING: verificar familia real + extensiones
        if lib == "STACKING" and parsed.subject and "UF[H" in parsed.subject:
            familia = rules.get("familia_real", [])
            extensiones = rules.get("extensiones", [])
            valid_uf = familia + extensiones
            h_match = re.search(r'UF\[H(\d+)\]', parsed.subject)
            if h_match:
                h_num = f"H{int(h_match.group(1)):02d}"
                if h_num not in valid_uf:
                    parsed.warnings.append(
                        f"Paradigma STACKING: UF[{h_num}] no está en "
                        f"la familia verificada. "
                        f"Familia real: H01 H02 H29 H30 H51 H52 H57 H58. "
                        f"Extensiones: H04 H23 H48."
                    )

        # SAMU: sujeto canónico
        if lib == "SAMU" and parsed.subject:
            valid_subs = rules.get("valid_subjects", [])
            if parsed.subject and parsed.subject not in valid_subs:
                parsed.warnings.append(
                    f"Paradigma SAMU (alto nivel): "
                    f"'{parsed.subject}' no es operador canónico. "
                    f"Válidos: @ @trust_matrix @human_early @human_later "
                    f"#rise #set $mon $tue $wed $thu $fri $sat $sun"
                )

        # GATE: validación de secuencia H03→H05→H56→H06
        if lib == "GATE":
            seq = ["H03", "H05", "H56", "H06"]
            h_match = re.search(r'UF\[H(\d+)\]', parsed.subject or "")
            if h_match:
                h_num = f"H{int(h_match.group(1)):02d}"
                if h_num not in seq:
                    parsed.warnings.append(
                        f"GATE: H{h_num} fuera de secuencia canónica H03→H05→H56→H06"
                    )

    def _check_delimiter_consistency_original(
        self, sentence: str, parsed: ParsedSentence
    ) -> None:
        """
        Verifica que los delimitadores de módulo sean consistentes.
        {módulo} no puede abrir con { y cerrar con ]
        (módulo) no puede abrir con ( y cerrar con }
        """
        # Buscar pares inconsistentes
        inconsistent = re.search(r'\{[^}]*\]', sentence)
        if inconsistent:
            parsed.warnings.append(
                f"Delimitador inconsistente: '{{' abre pero ']' cierra — "
                f"módulos WORK/SOCIAL usan {{módulo}}"
            )
        inconsistent2 = re.search(r'\([^)]*\}', sentence)
        if inconsistent2:
            parsed.warnings.append(
                f"Delimitador inconsistente: '(' abre pero '}}' cierra — "
                f"módulos CRYPTO usan (módulo)"
            )
        # [módulo] — abre con [ cierra con }
        inconsistent3 = re.search(r'\[[^\]]*\}', sentence)
        if inconsistent3:
            parsed.warnings.append(
                f"Delimitador inconsistente: '[' abre pero '}}' cierra — "
                f"módulos ACTIVITY/STACKING usan [módulo]"
            )
        # {módulo) — abre con { cierra con )
        inconsistent4 = re.search(r'\{[^}]*\)', sentence)
        if inconsistent4:
            parsed.warnings.append(
                "Delimitador inconsistente: '{' abre pero ')' cierra — "
                "módulos WORK/SOCIAL usan {módulo}"
            )

    def _detect_library(self, sentence: str, parsed: ParsedSentence) -> None:
        """Detecta la biblioteca soberana predominante."""
        # Primero verificar si hay biblioteca inválida al inicio
        first_word = sentence.strip().split()[0] if sentence.strip() else ""
        VALID_LIBS = [
            "TRUST","SOCIAL","CRYPTO","WORK","SAMU",
            "ACTIVITY","GATE","STACKING","METHOD"
        ]
        
        # Módulos TRUST válidos según corpus verificado
        VALID_TRUST_MODULES = [
            "foundation","scope","term","command","scenario",
            "event","element","ecosystem","management","language",
            "what","when","how","ku-chat","wu-mail","mu-store",
            "rabbit-faith","logistical-executive"
        ]
        if first_word.upper() not in VALID_LIBS:
            parsed.library = Library.UNKNOWN
            parsed.errors.append(
                f"Biblioteca '{first_word}' no reconocida. "
                f"Bibliotecas válidas: {', '.join(VALID_LIBS)}"
            )
            return
        
        # Si pasó validación inicial, detectar biblioteca válida
        # Verificar que la biblioteca detectada sea exacta
        if first_word.upper() in VALID_LIBS:
            for lib in Library:
                if lib.value == first_word.upper() and lib != Library.UNKNOWN:
                    parsed.library = lib
                    return
        # Detección por delimitador de objeto
        if re.search(r"\[", sentence):
            parsed.library = Library.TRUST
        elif re.search(r"\{", sentence):
            parsed.library = Library.SOCIAL
        elif re.search(r"\(", sentence):
            parsed.library = Library.CRYPTO

    def _extract_subject(self, sentence: str, parsed: ParsedSentence) -> None:
        """Extrae el sujeto antes de =><=."""
        # Prioridad 0: METHOD con delimitadores < >
        method_match = self._re_subject_method.search(sentence)
        if method_match:
            parsed.subject = method_match.group(1).strip()
            return
        # Prioridad 1: módulo CRYPTO con espacios (x y z)
        crypto_match = self._re_subject_crypto.search(sentence)
        if crypto_match:
            parsed.subject = crypto_match.group(1).strip()
            return
        # Prioridad 2: módulo WORK/SOCIAL {módulo}
        work_match = self._re_subject_work.search(sentence)
        if work_match:
            parsed.subject = work_match.group(1).strip()
            return
        # Prioridad 3: módulo ACTIVITY UF[H##]
        activity_match = self._re_subject_uf.search(sentence)
        if activity_match:
            parsed.subject = activity_match.group(1).strip()
            return
        # Prioridad 4: SAMU @/#/$
        samu_match = self._re_subject_samu.search(sentence)
        if samu_match:
            parsed.subject = samu_match.group(1).strip()
            return
        # Prioridad 5: módulo TRUST [módulo] o FOUNDATION
        trust_match = self._re_subject_trust.search(sentence)
        if trust_match:
            parsed.subject = trust_match.group(1).strip()
            return
        # Prioridad 6: palabra simple (fallback)
        word_match = re.search(
            r'(\b\w[\w_\-\.]*)\s*=><=', sentence
        )
        if word_match:
            parsed.subject = word_match.group(1).strip()

    def _extract_object(
        self, sentence: str, parsed: ParsedSentence
    ) -> None:
        """Extrae el objeto entre el verbo y el nudo."""
        obj_match = re.search(
            r"\.\.\s*(?:[\w_\-\.@<>]+)\s*\.\.\s+(.+?)(?:\s*--\[|\s*$)",
            sentence
        )
        if obj_match:
            obj_text = obj_match.group(1).strip()
            # Si el objeto empieza con -- es que está vacío
            # y el parser capturó el nudo como objeto
            if obj_text.startswith("--[") or obj_text == "[term]":
                parsed.warnings.append(
                    "Objeto ausente — la acción no tiene "
                    "sobre qué operar."
                )
            else:
                parsed.obj = obj_text
        elif parsed.verb:
            # Hay verbo pero no hay objeto extraíble
            parsed.warnings.append(
                "Objeto ausente — la acción no tiene "
                "sobre qué operar."
            )

    def validate(self, sentence: str, _depth: int = 0) -> ParsedSentence:
        """
        Valida una sentencia LACHO soberanamente.
        _depth: TASK_1.2 DECIDABILITY_GUARD — max 64
        """
        if _depth >= MAX_RECURSION_DEPTH:
            p = ParsedSentence(sentence)
            p.errors.append(
                "ABORT: max recursion depth 64 exceeded — HALTING_PROBLEM guard [H06]"
            )
            return p

        # ── TASK_3.5 — DEPENDENT_CONTRACT pre-conditions ────────────────
        # PRE_1: sentence has at least 6 tokens
        _tokens = sentence.strip().split() if sentence.strip() else []
        if len(_tokens) < 6:
            p = ParsedSentence(sentence)
            p.errors.append(
                f"PRE_CONDITION_FAIL [PRE_1]: sentence has {len(_tokens)} tokens, "
                f"need >= 6 (SENTENCE ::= LIBRARY SUBJECT BIND VERB OBJECT KNOT TERM)"
            )
            return p

        # PRE_2: [term] marker present
        if "[" not in sentence or "]" not in sentence:
            p = ParsedSentence(sentence)
            p.errors.append(
                "PRE_CONDITION_FAIL [PRE_2]: [term] bracket not found in sentence"
            )
            return p

        verify_sovereign_conditions("grammar")

        sentence = sentence.strip()
        parsed = ParsedSentence(sentence)

        if not sentence:
            parsed.errors.append(
                "Sentencia vacía — no hay nada que validar."
            )
            return parsed

        # Aplicar todas las reglas
        self._check_connector(sentence, parsed)
        if parsed.errors:
            return parsed  # short-circuit: sin =><= nada más parsea
        self._detect_library(sentence, parsed)
        self._extract_subject(sentence, parsed)
        self._check_verb(sentence, parsed)
        self._extract_object(sentence, parsed)
        # Advertencias suaves de verbo/sujeto — no invalidan
        self._warn_verb_mismatch(parsed)
        self._warn_subject_mismatch(parsed)
        self._check_knot_and_term(sentence, parsed)
        self._check_delimiter_consistency_original(sentence, parsed)
        self._validate_by_paradigm(sentence, parsed)

        # CJK detection — unicode_mode CHINA
        cjk_found = []
        for zh, data in CJK_TOKEN_MAP.items():
            if zh in sentence:
                cjk_found.append(resolve_chinese_token(zh))
        if cjk_found:
            parsed.unicode_mode = "CHINA"
            parsed.cjk_tokens = cjk_found
        
        # Taxonomy
        parsed.taxonomy = classify_sentence(parsed)

        return parsed

    def suggest_correction(
        self, parsed: ParsedSentence
    ) -> str:
        hints = []
        raw = parsed.raw if parsed.raw else ""

        if "=><=" not in raw:
            hints.append("Agregar: =><= .. VERBO ..")
        if not parsed.verb:
            hints.append("Estructura: =><= .. VERBO .. OBJETO")
        if not parsed.knot:
            hints.append("Cerrar con: --[As de Guía]")
        elif any(
            kw in e for e in parsed.errors
            for kw in ["canónico", "no reconocido", "no es canónico"]
        ):
            hints.append(
                "Nudo mal escrito — forma exacta requerida: "
                "As de Guía / Nudo de Ocho / Ballestrinque / "
                "Nudo Corredizo / Nudo de Rizo"
            )
        if not parsed.term_present:
            hints.append("Agregar al final: [term]")
        if parsed.library.value == "UNKNOWN":
            hints.append(
                "Comenzar con biblioteca válida: "
                "TRUST / WORK / SAMU / CRYPTO / "
                "ACTIVITY / GATE / STACKING / SOCIAL / METHOD"
            )
        if not parsed.obj and parsed.verb:
            hints.append("Agregar objeto: =><= .. VERBO .. OBJETO --")

        return " | ".join(hints) if hints else "Sin errores detectados."

    def validate_batch(self, sentences: list[str]) -> list[ParsedSentence]:
        """Valida un lote de sentencias soberanamente."""
        return [self.validate(s) for s in sentences]


VERBOS_CANONICOS_LACHO = {
    "verifica","declara","sostiene","autoriza","limita",
    "ejecuta","detiene","procesa","activa","suspende",
    "protege","cifra","audita","firma","valida",
    "registra","evalúa","dirime","cristaliza",
    "penetra","emerge","completa","inicia","transita",
    "bloquea","abre","filtra","contiene","permite",
    "apila","inmutabiliza","consolida","ancla","reserva",
    "lanza","planifica","conecta","transmite","enmascara",
    "calcula","modela","deriva","simula","proyecta"
}

def lacho_score(parsed) -> float:
    """LACHO_SCORE — calidad soberana 0.0→1.0."""
    if getattr(parsed, "result", "INVALID") == "INVALID":
        return 0.0
    score = 0.5
    if (getattr(parsed, "verb", "") or "").lower() in VERBOS_CANONICOS_LACHO:
        score += 0.1
    warnings = getattr(parsed, "warnings", []) or []
    if not any("sujeto" in w.lower() for w in warnings):
        score += 0.1
    if getattr(parsed, "knot", "") in {
        "As de Guía","Nudo de Ocho","Ballestrinque",
        "Nudo Corredizo","Nudo de Rizo"}:
        score += 0.1
    if not warnings:
        score += 0.1
    if getattr(parsed, "tomo_id", None):
        score += 0.1
    
    # CJK bonus
    if getattr(parsed, 'unicode_mode', 'STANDARD') == 'CHINA':
        score += 0.05
    
    return round(min(score, 1.0), 3)


# ── Instancia global soberana ─────────────────────────────────────
_validator = GrammarValidator()

def validate(sentence: str, _depth: int = 0) -> ParsedSentence:
    """API pública soberana del validador. _depth: TASK_1.2"""
    return _validator.validate(sentence, _depth=_depth)


# ── Test soberano de arranque ─────────────────────────────────────
if __name__ == "__main__":
    test_sentences = [
        # Válida canónica
        "TRUST FOUNDATION =><= .. verifica .. [scope]_activo --[As de Guía] [term]",
        # Sin [term]
        "SAMU @ =><= .. dirime .. tension_soberana --[Nudo de Ocho]",
        # Sin nudo
        "ACTIVITY UF[H01] =><= .. inicia .. genesis_soberana [term]",
        # Válida compleja
        "WORK {doorman-mobile} =><= .. custodia .. actor_verificado --[Nudo Corredizo] [term]",
    ]

    validator = GrammarValidator()
    print("═" * 60)
    print("DIRIME IMV — Validador de Gramática Viva LACHO")
    print("═" * 60)
    for s in test_sentences:
        result = validator.validate(s)
        print(f"\n[{result.result.value}]")
        print(result.summary())
    print("\n═" * 60)
