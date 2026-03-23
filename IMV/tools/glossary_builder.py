"""
IMV/tools/glossary_builder.py
GAP_9 GLOSSARY_MANUAL — scans *.index.lacho files and produces unified glossary JSON.
Format discovered: entries are comment blocks starting with "## TERM [N1]"
[P2][I2] — closes GAP_9
"""
from __future__ import annotations
import json
import re
from pathlib import Path

GLOSSARY_DIRS = [
    Path(__file__).parent.parent.parent / "DOC-ar" / "LACHO_glossary_updated",
    Path(__file__).parent.parent.parent / "glossary",
    Path(__file__).parent.parent.parent / "CORPUS" / "GLOSSARY",
]
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "glossary_unified.json"


def parse_lacho_index(path: Path) -> list[dict]:
    """
    Parse .index.lacho file. Format:
      ## TERM [N1]
      # Clase: biblioteca · Nivel: 1 · scalar_min: 0.88
      # Description prose...
      # Delimitador: !! !!
      # Sujeto canónico: UF[H##]
      # Verbos: verb1 · verb2
      # Ejemplo: TRUST ...
    """
    entries: list[dict] = []
    current: dict = {}
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return entries

    for line in lines:
        stripped = line.strip()

        # Entry header: ## TERM [N1] or ## TERM
        m = re.match(r'^##\s+([A-Za-z_{}@#$\-\.\'\"\s]+?)\s*(?:\[N(\d)\])?\s*$', stripped)
        if m:
            if current.get("term"):
                entries.append(current)
            current = {
                "term": m.group(1).strip(),
                "level": int(m.group(2)) if m.group(2) else None,
                "source": path.stem,
                "libraries": [],
                "hexagrams": [],
                "verbs": [],
                "description": [],
            }
            continue

        if not current.get("term"):
            continue

        # Skip non-comment lines or empty
        if not stripped.startswith("#"):
            continue
        content = stripped.lstrip("#").strip()

        # Clase / nivel / scalar_min
        if content.startswith("Clase:"):
            current["clase"] = content
            # Extract library from clase line
            libs = re.findall(r'\b(TRUST|SAMU|CRYPTO|GATE|STACKING|WORK|SOCIAL|METHOD|ACTIVITY|COGNITIVO)\b', content)
            current["libraries"].extend(libs)
            continue

        # Delimitador
        if content.startswith("Delimitador:"):
            current["delimiter"] = content.replace("Delimitador:", "").strip()
            continue

        # Sujeto canónico
        if content.startswith("Sujeto canónico:") or content.startswith("Sujeto"):
            current["subject"] = content.split(":", 1)[-1].strip()
            hexes = re.findall(r'H\d+', content)
            current["hexagrams"].extend(hexes)
            continue

        # Verbos
        if content.startswith("Verbos:") or content.startswith("Verbo"):
            verbs = [v.strip() for v in content.split(":", 1)[-1].split("·") if v.strip()]
            current["verbs"].extend(verbs)
            continue

        # UF activos
        if content.startswith("UF activos:") or content.startswith("UF["):
            hexes = re.findall(r'H\d+', content)
            current["hexagrams"].extend(hexes)
            continue

        # Ejemplo (canonical sentence)
        if content.startswith("Ejemplo:"):
            current["example"] = content.replace("Ejemplo:", "").strip()
            continue

        # scalar_min standalone
        m_s = re.search(r'scalar_min:\s*([\d.]+)', content)
        if m_s:
            current["scalar_min"] = float(m_s.group(1))

        # Description prose (any other comment line with content)
        if content and not content.startswith("#") and len(content) > 3:
            current["description"].append(content)

    if current.get("term"):
        entries.append(current)

    # Clean up description
    for e in entries:
        e["description"] = " ".join(e["description"][:3])  # first 3 lines only
        # Deduplicate hexagrams
        e["hexagrams"] = sorted(set(e["hexagrams"]))
        e["verbs"] = list(dict.fromkeys(e["verbs"]))  # deduplicate preserving order

    return entries


def build_glossary() -> dict:
    unified: dict[str, dict] = {}
    files_scanned = 0

    for d in GLOSSARY_DIRS:
        if not d.exists():
            continue
        for f in sorted(d.rglob("*.index.lacho")):
            entries = parse_lacho_index(f)
            files_scanned += 1
            for e in entries:
                term = e.get("term", "").strip()
                if not term or len(term) > 80:
                    continue
                if term not in unified:
                    unified[term] = e
                else:
                    # Merge: add alt source, extend hexagrams and verbs
                    ex = unified[term]
                    ex.setdefault("alt_sources", []).append(e.get("source", ""))
                    for h in e.get("hexagrams", []):
                        if h not in ex.get("hexagrams", []):
                            ex.setdefault("hexagrams", []).append(h)
                    for v in e.get("verbs", []):
                        if v not in ex.get("verbs", []):
                            ex.setdefault("verbs", []).append(v)

    return {
        "meta": {
            "total_terms": len(unified),
            "files_scanned": files_scanned,
            "generated_by": "glossary_builder.py — GAP_9 GLOSSARY_MANUAL",
            "format_version": "1.0",
        },
        "terms": dict(sorted(unified.items())),
    }


def write_glossary(output: Path | None = None) -> dict:
    out = output or OUTPUT_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    glossary = build_glossary()
    out.write_text(json.dumps(glossary, indent=2, ensure_ascii=False), encoding="utf-8")
    return glossary


if __name__ == "__main__":
    result = write_glossary()
    meta = result["meta"]
    print(f"GAP_9 CLOSED: {meta['total_terms']} terms from {meta['files_scanned']} files")
    print(f"Output: {OUTPUT_PATH}")
    # Show sample
    terms = list(result["terms"].keys())
    print(f"Sample terms: {terms[:8]}")
