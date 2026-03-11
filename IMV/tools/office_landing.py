"""
IMV/tools/office_landing.py
Intérprete de directivas simbólicas LACHO · Office Landing
"""
from __future__ import annotations
import re, sys, time
from dataclasses import dataclass, field
from pathlib import Path

_IMV = Path(__file__).parent.parent
sys.path.insert(0, str(_IMV))
_BASE = _IMV.parent

from core.language_routing import route, RoutedSentence

DIRECTIVA_MAP = [
    (r"DOOR[_\.]",         "bloquear acceso no autorizado entrada soberana"),
    (r"GATE[_\.]",         "filtrar acceso riesgoso operacion"),
    (r"READER[_\.]",       "ejecutar lectura archivos lacho corpus"),
    (r"RUNNER[_\.]",       "ejecutar proceso automatizado soberano"),
    (r"FULLBACK[_\.]",     "ejecutar ciclo completo actividad soberana"),
    (r"SAMU[_\.]",         "auditar coherencia score soberano"),
    (r"LIBERAL[_\.]FRONT", "auditar recepcion entrada operador"),
    (r"BOOKER[_\.]",       "archivar registrar historial ledger"),
    (r"SMART[_\.]CONTRACT","verificar contrato digital soberano"),
    (r"TRUST[_\.]",        "verificar identidad contrato confianza"),
    (r"STREAMING[_\.]",    "transmitir conectar comunidad canal"),
    (r"TESSERACT[_\.]",    "calcular derivar modelar biblioteca lacho"),
    (r"MU[_\-]STORE",      "calcular modelar derivar libreria soberana"),
    (r"ACTIVITY[_\.]",     "iniciar activar ciclo soberano"),
    (r"PULSING[_\.]",      "iniciar activar elpulsar ciclo"),
    (r"KALIL[_\.]",        "iniciar nodo kalil economico"),
    (r"CEO[_\.]",          "declarar voluntad soberana trust foundation"),
    (r"ELPULSAR[_\.]",     "activar dashboard elpulsar operador"),
    (r"DIRIME[_\.]",       "auditar dirime motor decision soberano"),
    (r"LACHO[_\.]",        "verificar sentencia lacho gramatica"),
]

PRIORITY = {"TRUST":1,"GATE":2,"SAMU":3,"CRYPTO":4,
            "STACKING":5,"WORK":6,"METHOD":7,"ACTIVITY":8,"SOCIAL":9}

@dataclass
class Directiva:
    linea: int
    raw: str
    simbolo: str
    intencion: str
    routed: RoutedSentence | None = None

@dataclass
class PlanEjecucion:
    fuente: str
    timestamp: str
    directivas: list = field(default_factory=list)
    validas: int = 0
    total: int = 0

def _detectar(linea: str):
    lu = linea.upper()
    for patron, intencion in DIRECTIVA_MAP:
        if re.search(patron, lu):
            m = re.search(patron, lu)
            return m.group(0).rstrip("._-"), intencion
    return None

def interpretar(texto: str, fuente: str = "stdin") -> PlanEjecucion:
    plan = PlanEjecucion(fuente=fuente, timestamp=time.strftime("%Y-%m-%d %H:%M"))
    dirs = []
    for n, linea in enumerate(texto.splitlines(), 1):
        linea = linea.strip()
        if not linea or linea.startswith("#"): continue
        r = _detectar(linea)
        if not r: continue
        simbolo, intencion = r
        dirs.append(Directiva(n, linea, simbolo, intencion))
    plan.total = len(dirs)
    for d in dirs:
        d.routed = route(d.intencion)
        if d.routed.validated: plan.validas += 1
    dirs.sort(key=lambda d: PRIORITY.get(d.routed.library if d.routed else "ACTIVITY", 9))
    plan.directivas = dirs
    return plan

def render(plan: PlanEjecucion) -> str:
    pct = int(plan.validas / max(plan.total,1) * 100)
    lines = ["="*62,
             f"OFFICE LANDING · {plan.fuente}",
             f"{plan.total} directivas · {plan.validas} válidas · {pct}% soberano",
             "="*62]
    for d in plan.directivas:
        r = d.routed
        if not r: continue
        st = "✅" if r.validated else "⚠️ "
        cjk = f" CJK:{r.cjk_tokens}" if r.cjk_tokens else ""
        lines.append(f"\n[L{d.linea:02d}] {st} {d.simbolo:<20} [{r.library}] score={r.score:.2f}{cjk}")
        lines.append(f"  SYM: {d.raw[:55]}")
        lines.append(f"  →   {r.sentence}")
    lines += ["","="*62, f"PLAN · {plan.validas}/{plan.total} soberanas","="*62]
    return "\n".join(lines)

def render_compact(plan: PlanEjecucion) -> str:
    lines = [f"# OFFICE LANDING · {plan.fuente} · {plan.timestamp}",
             f"# {plan.validas}/{plan.total} soberanas",""]
    for i,d in enumerate(plan.directivas,1):
        if d.routed and d.routed.validated:
            lines += [f"# [{i}] {d.simbolo}", d.routed.sentence, ""]
    return "\n".join(lines)

if __name__ == "__main__":
    args = sys.argv[1:]
    if args and Path(args[0]).exists():
        archivo = Path(args[0])
    else:
        inbox = _BASE / "INBOX(gradient)"
        txts = list(inbox.glob("*.txt")) if inbox.exists() else []
        if not txts:
            print("Sin archivo. Uso: python3 tools/office_landing.py [archivo.txt]")
            sys.exit(1)
        archivo = txts[0]
    plan = interpretar(archivo.read_text(errors="ignore"), archivo.name)
    print(render(plan))
    out = _BASE / "JOURNAL" / f"PLAN_{archivo.stem[:40]}.lacho"
    out.parent.mkdir(exist_ok=True)
    out.write_text(render_compact(plan))
    print(f"\n💾 {out.name}")
