#!/usr/bin/env python3
"""
generator.py — IMV genera su primer .lacho soberano
SUITE SOBERANA · VECTOR 1 · 2026-03-10
Uso: python3 tools/generator.py [--mode auto|stats|corpus|full] [--output path]
"""

STYLE = {"font": "monospace", "bg": "#FFFFFF", "fg": "#000000"}

import sys, argparse
from pathlib import Path
from datetime import datetime

# ── paths ─────────────────────────────────────────────────────
ROOT       = Path(__file__).parent.parent
OUTPUT_DIR = ROOT.parent / "LACHO_FILES"
OUTPUT_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(ROOT))

# ── imports soberanos ─────────────────────────────────────────
from core.grammar        import validate, lacho_score, VERBOS_NATURALES, SUJETOS_CANONICOS
from core.ledger         import get_stats, get_recent, export_crystals_report
from core.ledger         import get_verb_frequency, get_library_stats
from core.language_routing import route

# ── constantes ────────────────────────────────────────────────
VERSION = "0.1"
KNOT_DEFAULT = {
    "TRUST": "Nudo de Ocho", "STACKING": "Nudo de Ocho",
    "SAMU": "Ballestrinque", "GATE": "Nudo Corredizo",
    "WORK": "As de Guía", "ACTIVITY": "As de Guía",
    "CRYPTO": "Nudo de Ocho", "SOCIAL": "As de Guía",
    "METHOD": "Ballestrinque",
}

# ══════════════════════════════════════════════════════════════
# PASO 1 — COLLECT
# ══════════════════════════════════════════════════════════════
def collect():
    stats    = get_stats()
    recent   = get_recent(20)
    crystals = export_crystals_report()
    lib_st   = get_library_stats()
    verb_fr  = get_verb_frequency(10)
    return {
        "stats":    stats,
        "recent":   recent,
        "crystals": crystals,
        "lib_stats": lib_st,
        "verb_freq": verb_fr,
    }

# ══════════════════════════════════════════════════════════════
# PASO 2 — ROUTE · traducir datos a sentencias LACHO
# ══════════════════════════════════════════════════════════════
def build_stats_sentences(data: dict) -> list[str]:
    s  = data["stats"]
    tx = s.get("transactions_total", 0)
    sc = s.get("lacho_score", 0)
    cr = s.get("crystals_total", 0)
    gv = s.get("grammar_valid", 0)
    gr = s.get("green_count", 0)

    return [
        f"METHOD <stat_onto> =><= .. calcula .. TX_{tx}_soberano --[As de Guía] [term]",
        f"STACKING UF[H52] =><= .. cristaliza .. scalar_s_{sc}_activo --[Nudo de Ocho] [term]",
        f"SAMU @ =><= .. audita .. cristales_{cr}_verificados --[Ballestrinque] [term]",
        f"METHOD <stat_onto> =><= .. calcula .. grammar_valid_{gv}_sentencias --[As de Guía] [term]",
        f"STACKING UF[H52] =><= .. consolida .. green_{gr}_WU_activos --[Nudo de Ocho] [term]",
    ]

def build_recent_sentences(data: dict) -> list[str]:
    out = []
    for tx in data["recent"]:
        td = tx.data if isinstance(tx.data, dict) else {}
        if td.get("result") == "VALID":
            s = td.get("sentence", "")
            if s:
                parsed = validate(s)
                if parsed.result == "VALID":
                    out.append(s)
                    if len(out) >= 8:
                        break
    return out

def build_crystal_sentences(data: dict) -> list[str]:
    out = []
    rep = data["crystals"]
    crystals = rep.get("crystals", []) if isinstance(rep, dict) else []
    for c in crystals[:8]:
        content = c.get("content", "") or c.get("form", "")
        if not content:
            continue
        try:
            r = route(content)
            lib  = r.library
            subj = SUJETOS_CANONICOS.get(lib, ["FOUNDATION"])[0]
            verb = VERBOS_NATURALES.get(lib, ["verifica"])[0]
            knot = KNOT_DEFAULT.get(lib, "As de Guía")
            obj  = content.replace(" ", "_").replace("/", "_")[:40]
            s = f"{lib} {subj} =><= .. {verb} .. {obj} --[{knot}] [term]"
            parsed = validate(s)
            if parsed.result in ("VALID", "WARNING"):
                out.append(s)
        except Exception:
            continue
    return out

def build_lib_sentences(data: dict) -> list[str]:
    out = []
    for ls in data["lib_stats"][:5]:
        lib   = ls.get("library", "METHOD")
        count = ls.get("count", 0)
        subj  = SUJETOS_CANONICOS.get(lib, ["FOUNDATION"])[0]
        verb  = VERBOS_NATURALES.get(lib, ["verifica"])[0]
        knot  = KNOT_DEFAULT.get(lib, "As de Guía")
        s = f"{lib} {subj} =><= .. {verb} .. lib_{lib.lower()}_uso_{count} --[{knot}] [term]"
        out.append(s)
    return out

# ══════════════════════════════════════════════════════════════
# PASO 3 — SELECT · filtrar WU
# ══════════════════════════════════════════════════════════════
def select_valid(sentences: list[str], threshold: float = 0.6) -> list[str]:
    out = []
    for s in sentences:
        try:
            parsed = validate(s)
            sc = lacho_score(parsed)
            if parsed.result in ("VALID", "WARNING") and sc >= threshold:
                out.append((sc, s))
        except Exception:
            continue
    out.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in out]

# ══════════════════════════════════════════════════════════════
# PASO 4 — COMPOSE
# ══════════════════════════════════════════════════════════════
def cabecera(stats: dict, ts: str, avg: float, n: int) -> str:
    return f"""//[genesis]   :: IMV AUTO-GENERATED
//[version]   :: {VERSION}
//[tipo]      :: GENERATED · AUTO
//[fecha]     :: {ts}
//[tx_total]  :: {stats.get('transactions_total', 0)}
//[cristales] :: {stats.get('crystals_total', 0)}
//[score_avg] :: {avg:.3f}
//[sentences] :: {n}
//[term]      :: activo
//空聽數 · MU→KU→WU · DIR(=)
"""

def bloque(titulo: str, sentences: list[str]) -> str:
    if not sentences:
        return ""
    lines = "\n".join(sentences)
    return f"\n// ── {titulo} {'─' * (50 - len(titulo))}\n{lines}\n"

def anclas_rag(ts: str) -> str:
    ts_clean = ts.replace(":", "").replace("-", "").replace(" ", "_")
    return f"""
// ── ANCLAS RAG AUTOGENERADAS {'─' * 24}
METHOD <operator_flow> =><= .. ejecuta .. generated_lacho_{ts_clean} --[As de Guía] [term]
STACKING UF[H52] =><= .. inmutabiliza .. lacho_generado_wu_{ts_clean} --[Nudo de Ocho] [term]
SAMU @ =><= .. audita .. generator_py_output_{ts_clean} --[Ballestrinque] [term]
TRUST FOUNDATION =><= .. declara .. imv_vivo_primer_lacho --[Nudo de Ocho] [term]

//DIR(=) GENERADO · IMV VIVO · {ts}
"""

def pie(ts: str, n: int, avg: float) -> str:
    return f"//DIR(=) {n} sentencias · score {avg:.3f} · {ts}\n"

def compose(mode: str, data: dict, ts: str) -> str:
    stats_s   = build_stats_sentences(data)
    recent_s  = build_recent_sentences(data)
    crystal_s = build_crystal_sentences(data)
    lib_s     = build_lib_sentences(data)

    # selección por modo
    if mode == "stats":
        all_s = stats_s
    elif mode == "corpus":
        all_s = crystal_s + lib_s
    elif mode == "auto":
        all_s = recent_s + stats_s[:3]
    else:  # full
        all_s = stats_s + recent_s + crystal_s + lib_s

    valid = select_valid(all_s)

    if not valid:
        # fallback garantizado
        valid = [
            "TRUST FOUNDATION =><= .. declara .. imv_generator_activo --[Nudo de Ocho] [term]",
            "METHOD <stat_onto> =><= .. calcula .. sistema_soberano_operativo --[As de Guía] [term]",
            "STACKING UF[H52] =><= .. cristaliza .. primer_lacho_generado --[Nudo de Ocho] [term]",
        ]

    scores = []
    for s in valid:
        try:
            parsed = validate(s)
            scores.append(lacho_score(parsed))
        except Exception:
            scores.append(0.5)
    avg = round(sum(scores) / len(scores), 3) if scores else 0.0

    content  = cabecera(data["stats"], ts, avg, len(valid))
    content += bloque("ESTADO SISTEMA", stats_s[:5])
    if mode in ("auto", "full"):
        content += bloque("TX RECIENTES VÁLIDAS", recent_s[:5])
    if mode in ("corpus", "full"):
        content += bloque("CRISTALES FRECUENTES", crystal_s[:5])
        content += bloque("BIBLIOTECAS ACTIVAS", lib_s[:5])
    content += anclas_rag(ts)
    content += pie(ts, len(valid), avg)

    return content, valid, avg

# ══════════════════════════════════════════════════════════════
# PASO 5+6 — VALIDATE + WRITE
# ══════════════════════════════════════════════════════════════
def write_file(content: str, output_path: Path) -> None:
    output_path.write_text(content, encoding="utf-8")

def register_crystal(ts: str, path: Path) -> None:
    try:
        from core.ledger import record_crystal
        ts_id = ts.replace(":", "").replace("-", "").replace(" ", "_")
        record_crystal(
            crystal_id=f"GEN_{ts_id}",
            form="GENERATED_LACHO",
            content=f"generator.py → {path.name}",
            frequency=1
        )
    except Exception as e:
        print(f"  ⚠ ledger record: {e}")

# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="IMV generator — genera .lacho soberano")
    parser.add_argument("--mode",   default="stats",
                        choices=["auto","stats","corpus","full"],
                        help="modo de generación")
    parser.add_argument("--output", default=None,
                        help="ruta de salida (opcional)")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ts_human = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n⬡ GENERATOR · mode={args.mode} · {ts_human}")
    print("  PASO 1 · collect...")
    data = collect()
    print(f"         TX:{data['stats']['transactions_total']} · cristales:{data['stats']['crystals_total']} · recent:{len(data['recent'])}")

    print("  PASO 2+3 · compose + select...")
    content, valid, avg = compose(args.mode, data, ts_human)
    print(f"         {len(valid)} sentencias · score_avg:{avg}")

    # validación batch
    scores = [lacho_score(validate(s)) for s in valid]
    avg_check = round(sum(scores)/len(scores), 3) if scores else 0
    if avg_check < 0.55:
        print(f"  ⚠ score bajo ({avg_check}) · usando fallback")

    print("  PASO 4 · write...")
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = OUTPUT_DIR / f"generated_{ts}.lacho"

    write_file(content, out_path)
    print(f"         {out_path}")

    print("  PASO 5 · ledger record...")
    register_crystal(ts_human, out_path)

    print(f"\n✅ generado: {out_path.name}")
    print(f"   {len(valid)} sentencias · score {avg} · mode={args.mode}")
    print(f"   {out_path}\n")

if __name__ == "__main__":
    main()
