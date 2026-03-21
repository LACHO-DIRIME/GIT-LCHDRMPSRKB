#!/usr/bin/env python3
"""
tools/autoresearch_specs.py — Scanner soberano del ecosistema DIRIME.
Sin Groq · Python stdlib puro · genera actual_structure.json + sorted_upgrading.yml
[term] :: activo
"""

STYLE = {"font": "monospace", "bg": "#FFFFFF", "fg": "#000000"}

import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime

REPO_ROOT  = Path(__file__).parent.parent
IMV_ROOT   = REPO_ROOT / "IMV"
ASKINGS_DIR = REPO_ROOT / "Askings for autoresearching by technical horizons"

def scan_filesystem() -> dict:
    """Clasifica módulos Python: ACTIVE / DECLARED / STUB / BLOCKED."""
    modules = {}
    capa_c = {"ime", "cat_local", "ollama_bridge"}

    for py in list((IMV_ROOT / "core").glob("*.py")) + \
              list((IMV_ROOT / "tools").glob("*.py")) + \
              list((REPO_ROOT / "tools").glob("*.py")) + \
              list((REPO_ROOT / "DIRIME_v2").rglob("*.py")):
        rel = str(py.relative_to(REPO_ROOT))
        size = py.stat().st_size
        if any(c in rel for c in capa_c):
            status = "BLOCKED"
        elif size < 50:
            status = "STUB"
        elif size > 500:
            status = "ACTIVE"
        else:
            status = "DECLARED"
        modules[rel] = {"status": status, "size": size}
    return modules

def scan_sovereign_db() -> dict:
    """Lee métricas del ledger soberano."""
    db = IMV_ROOT / "data" / "sovereign.db"
    if not db.exists():
        return {}
    try:
        sys.path.insert(0, str(IMV_ROOT))
        from DIRIME_v2.fabric.poke_peek import peek
        scalar = peek("scalar_s") or "?"
    except Exception:
        scalar = "?"
    with sqlite3.connect(db) as conn:
        tx    = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
        cryst = conn.execute("SELECT COUNT(*) FROM crystals").fetchone()[0]
        verbs = conn.execute(
            "SELECT json_extract(data,'$.verb'), COUNT(*) FROM transactions "
            "WHERE type='GRAMMAR_VALIDATION' GROUP BY 1 ORDER BY 2 DESC LIMIT 10"
        ).fetchall()
    return {
        "tx_total": tx, "crystals": cryst,
        "scalar_s": scalar,
        "verb_freq_top10": [{"verb": v, "count": c} for v, c in verbs if v]
    }

def scan_corpus_gaps() -> list:
    """Detecta tokens UNICODE declarados sin implementación Python."""
    gaps = []
    unicode_dir = REPO_ROOT / "CORPUS" / "UNICODE PROGRAMS"
    if not unicode_dir.exists():
        return gaps
    all_py = set()
    for py in (IMV_ROOT / "core").glob("*.py"):
        all_py.add(py.read_text(errors="ignore").lower())
    for txt in unicode_dir.glob("*.txt"):
        content = txt.read_text(errors="ignore")
        for line in content.splitlines():
            if line.startswith("def ") or "_FUNC:" in line or "_PY:" in line:
                func = line.split("(")[0].replace("def ","").strip().lower()
                if func and not any(func in py for py in all_py):
                    gaps.append(f"{txt.name} → {func} sin implementación Python")
    # gaps conocidos hardcodeados
    known = [
        "scalar_s:0 en /api/notaria/archivo · guardar en data al registrar grammar",
        "sync:0 cristales elpulsar startup · sync_from_ledger apuntar a sovereign.db IMV",
        "github_sync.sh commit message usa TX/S hardcodeados en vez de valores reales",
    ]
    return known + gaps[:10]

def generate_actual_structure(modules: dict, db: dict) -> Path:
    out = {
        "generated": datetime.now().isoformat(),
        "tx_total": db.get("tx_total", 0),
        "crystals": db.get("crystals", 0),
        "scalar_s": db.get("scalar_s", "?"),
        "modules": modules,
        "verb_freq": db.get("verb_freq_top10", []),
    }
    path = ASKINGS_DIR / "actual_structure.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return path

def generate_sorted_upgrading(modules: dict, gaps: list) -> Path:
    active    = [k for k,v in modules.items() if v["status"]=="ACTIVE"]
    declared  = [k for k,v in modules.items() if v["status"]=="DECLARED"]
    stubs     = [k for k,v in modules.items() if v["status"]=="STUB"]
    blocked   = [k for k,v in modules.items() if v["status"]=="BLOCKED"]
    lines = [
        "# sorted_upgrading.yml — generado por autoresearch_specs.py",
        f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "modules:",
        "  ACTIVE:",
    ]
    for m in active[:15]: lines.append(f"    - {m}")
    lines += ["  DECLARED:"]
    for m in declared[:10]: lines.append(f"    - {m}")
    lines += ["  STUB:"]
    for m in stubs[:10]: lines.append(f"    - {m}")
    lines += ["  BLOCKED:"]
    for m in blocked[:10]: lines.append(f"    - {m}")
    lines += ["", "gaps:"]
    for g in gaps: lines.append(f"  - \"{g}\"")
    path = ASKINGS_DIR / "sorted_upgrading.yml"
    path.write_text("\n".join(lines))
    return path

def main():
    print("⬡ autoresearch_specs.py · scanner soberano")
    print("  PASO 1 · filesystem...")
    modules = scan_filesystem()
    active  = sum(1 for v in modules.values() if v["status"]=="ACTIVE")
    print(f"         {len(modules)} módulos · {active} ACTIVE")
    print("  PASO 2 · sovereign.db...")
    db = scan_sovereign_db()
    print(f"         TX={db.get('tx_total','?')} · cristales={db.get('crystals','?')} · S={db.get('scalar_s','?')}")
    print("  PASO 3 · corpus gaps...")
    gaps = scan_corpus_gaps()
    print(f"         {len(gaps)} gaps detectados")
    print("  PASO 4 · escribir outputs...")
    p1 = generate_actual_structure(modules, db)
    p2 = generate_sorted_upgrading(modules, gaps)
    print(f"         {p1.name} · {p2.name}")
    print("✅ specs completo")

if __name__ == "__main__":
    main()
