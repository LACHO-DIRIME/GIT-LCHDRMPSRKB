"""
IMV/core/language_routing.py
Bridge NLP → LACHO · Sesión 9 · 2026-03-09 · Fix $wed 2026-03-11
Toma texto natural y lo convierte en sentencia LACHO válida.
Pipeline: texto → intent → biblioteca → sujeto → verbo → objeto → sentencia
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.grammar import (
    validate, is_chinese, CJK_TOKEN_MAP,
    SUJETOS_CANONICOS, VERBOS_CANONICOS_LACHO,
    ValidationResult
)

# ── TABLA DE INTENT ──────────────────────────────────────────
# Palabras clave en español/inglés → biblioteca LACHO

INTENT_MAP: dict[str, list[str]] = {
    "TRUST":    ["contrato","firmar","verificar","identidad","escritura",
                 "notaría","notaria","registro","validar","certificar","confianza"],
    "CRYPTO":   ["wallet","crypto","bitcoin","ethereum","token","blockchain",
                 "custodia","llave","clave","cifrar","usdt","e-cny"],
    "SAMU":     ["auditar","revisar","disputa","conflicto","score","rating",
                 "evaluar","evalúa","coherencia","scalar","nora","面子"],
    "GATE":     ["bloquear","filtrar","esperar","acceso","entrada","permiso",
                 "riesgo","peligro","emergencia","detener","freno"],
    "STACKING": ["archivar","guardar","cristal","inmutable","preservar",
                 "historial","registrar","anclar","apilar","ledger"],
    "WORK":     ["ejecutar","correr","proceso","automatizar","bot","actuador",
                 "tarea","flujo","workflow","github","sync"],
    "SOCIAL":   ["lanzar","publicar","comunidad","red","wechat","alipay",
                 "diaspora","remesa","conectar","transmitir","marketing"],
    "METHOD":   ["calcular","modelar","proyectar","simular","ecuación",
                 "derivar","ratio","métrica","formula","algoritmo"],
    "ACTIVITY": ["iniciar","comenzar","activar","arrancar","emerger",
                 "completar","ciclo","hexagrama","phase","fase"],
}

# Verbo por defecto para cada biblioteca
DEFAULT_VERB: dict[str, str] = {
    "TRUST":    "verifica",
    "CRYPTO":   "protege",
    "SAMU":     "audita",
    "GATE":     "filtra",
    "STACKING": "inmutabiliza",
    "WORK":     "ejecuta",
    "SOCIAL":   "conecta",
    "METHOD":   "calcula",
    "ACTIVITY": "inicia",
}

# Sujeto por defecto para cada biblioteca
DEFAULT_SUBJECT: dict[str, str] = {
    "TRUST":    "FOUNDATION",
    "CRYPTO":   "(key seat)",
    "SAMU":     "@",
    "GATE":     "UF[H05]",
    "STACKING": "UF[H52]",
    "WORK":     "{actuator}",
    "SOCIAL":   "{relay}",
    "METHOD":   "<equation>",
    "ACTIVITY": "UF[H57]",
}

# Nudo por defecto según tono del texto
DEFAULT_KNOT = "As de Guía"
KNOT_RISK_WORDS = {"riesgo","peligro","bloquear","emergencia","conflicto",
                   "disputa","detener","freno","brake","colapso"}
KNOT_SEAL_WORDS = {"inmutable","archivar","cristal","sellado","preservar",
                   "historial","anclar","registro"}
KNOT_TENSION_WORDS = {"auditar","evaluar","evalúa","rating","score","disputa",
                      "revisar","coherencia","conflicto"}


@dataclass
class RoutedSentence:
    raw_input:  str
    library:    str
    subject:    str
    verb:       str
    obj:        str
    knot:       str
    sentence:   str          # sentencia LACHO final
    cjk_tokens: list[str]
    confidence: float        # 0.0-1.0
    validated:  bool
    score:      float
    notes:      list[str]


def _detect_library(text: str) -> tuple[str, float]:
    """Detecta biblioteca desde texto natural. Retorna (lib, confidence)."""
    tl = text.lower()
    scores: dict[str, int] = {}
    for lib, keywords in INTENT_MAP.items():
        hits = sum(1 for kw in keywords if kw in tl)
        if hits:
            scores[lib] = hits

    # CJK bonus
    for zh, data in CJK_TOKEN_MAP.items():
        if zh in text:
            lib = data[0] if isinstance(data, tuple) else data.get("library", "")
            if lib:
                scores[lib] = scores.get(lib, 0) + 2

    if not scores:
        return "METHOD", 0.3
    best = max(scores, key=lambda k: scores[k])
    confidence = min(0.5 + scores[best] * 0.1, 0.95)
    return best, confidence


def _detect_verb(text: str, library: str) -> str:
    """Detecta verbo canónico desde texto. Si no hay match, usa default."""
    tl = text.lower()
    # Buscar verbo canónico directo en el texto
    for v in VERBOS_CANONICOS_LACHO:
        if v in tl:
            return v
    return DEFAULT_VERB.get(library, "ejecuta")


def _detect_knot(text: str) -> str:
    """Detecta nudo apropiado según palabras de riesgo/tensión/sellado."""
    tl = text.lower()
    if any(w in tl for w in KNOT_RISK_WORDS):
        return "Nudo Corredizo"
    if any(w in tl for w in KNOT_SEAL_WORDS):
        return "Nudo de Ocho"
    if any(w in tl for w in KNOT_TENSION_WORDS):
        return "Ballestrinque"
    return "As de Guía"


def _extract_object(text: str, library: str, cjk_tokens: list[str]) -> str:
    """Extrae objeto semántico del texto. Usa CJK si hay tokens."""
    # Si hay token CJK, usarlo como núcleo del objeto
    if cjk_tokens:
        base = cjk_tokens[0]
        # sanitizar texto para objeto LACHO
        clean = re.sub(r'[^\w\u4e00-\u9fff_]', '_', text.lower())[:30]
        return f"{base}_{clean}".strip("_")

    # Extraer palabras clave (sustantivos candidatos)
    stop = {"el","la","los","las","un","una","de","del","que","en",
            "con","por","para","es","son","hay","se","yo","tu","su"}
    words = [w for w in re.sub(r'[^\w\s]','',text.lower()).split()
             if w not in stop and len(w) > 3]
    if words:
        obj = "_".join(words[:3])
    else:
        obj = f"operacion_{library.lower()}"
    return obj[:40]


def route(text: str) -> RoutedSentence:
    """
    Convierte texto natural a sentencia LACHO válida.

    Uso:
        from core.language_routing import route
        r = route("necesito verificar un contrato digital")
        print(r.sentence)
    """
    notes = []

    # 1. Detectar CJK tokens
    cjk_tokens = [zh for zh in CJK_TOKEN_MAP if zh in text]

    # 2. Detectar biblioteca
    library, confidence = _detect_library(text)
    notes.append(f"library={library} confidence={confidence:.2f}")

    # 3. Sujeto
    subject = DEFAULT_SUBJECT.get(library, "FOUNDATION")

    # 4. Verbo
    verb = _detect_verb(text, library)

    # 5. Objeto
    obj = _extract_object(text, library, cjk_tokens)

    # 6. Nudo
    knot = _detect_knot(text)

    # 7. Construir sentencia
    sentence = f"{library} {subject} =><= .. {verb} .. {obj} --[{knot}] [term]"

    # 8. Validar con grammar
    parsed = validate(sentence)
    validated = parsed.result in (ValidationResult.VALID, ValidationResult.WARNING)

    from core.grammar import lacho_score
    score = lacho_score(parsed)

    if not validated:
        notes.append(f"INVALID: {parsed.errors}")
        # Intentar fallback con verbo/sujeto defaults puros
        sentence = (f"{library} {DEFAULT_SUBJECT[library]} =><= "
                    f".. {DEFAULT_VERB[library]} .. {obj} --[{DEFAULT_KNOT}] [term]")
        parsed = validate(sentence)
        validated = parsed.result != ValidationResult.INVALID
        score = lacho_score(parsed)
        notes.append("fallback aplicado")

    return RoutedSentence(
        raw_input  = text,
        library    = library,
        subject    = subject,
        verb       = verb,
        obj        = obj,
        knot       = knot,
        sentence   = sentence,
        cjk_tokens = cjk_tokens,
        confidence = confidence,
        validated  = validated,
        score      = score,
        notes      = notes,
    )


def route_batch(texts: list[str]) -> list[RoutedSentence]:
    """Procesa lista de textos en batch."""
    return [route(t) for t in texts]


def route_summary(r: RoutedSentence) -> str:
    """String resumen de un RoutedSentence."""
    status = "✅ VALID" if r.validated else "❌ INVALID"
    cjk = f" · CJK: {r.cjk_tokens}" if r.cjk_tokens else ""
    return (
        f"{status} [{r.library}] score={r.score:.2f} conf={r.confidence:.2f}{cjk}\n"
        f"  → {r.sentence}"
    )


# ── CLI directo ───────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    tests = [
        "necesito verificar un contrato digital de exportación",
        "auditar el score de coherencia del sistema",
        "bloquear acceso riesgoso a la wallet de custodia",
        "cristalizar el historial inmutable del período",
        "lanzar campaña de remesas para la diáspora china",
        "verificar 信任 en contrato dual exterior-interior",
        "calcular ratio riesgo lanzamiento 面子 nora score",
    ]

    if len(sys.argv) > 1:
        tests = [" ".join(sys.argv[1:])]

    print("=" * 60)
    print("LANGUAGE ROUTING — NLP → LACHO")
    print("=" * 60)
    for t in tests:
        r = route(t)
        print(f"\nINPUT: {t}")
        print(route_summary(r))
        if r.notes:
            print(f"  notes: {r.notes}")
    print("=" * 60)
