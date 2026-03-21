#!/usr/bin/env python3
"""
tools/chcl_runner.py — Ejecutor soberano de CHCL_BASE.txt
CHCL = Common Hypothetical Circumstances-based Language
CEO de LACHO · Portabilidad soberana · Estética COBOL
[term] :: activo · [seal of secrecy] :: activo
"""

STYLE = {"font": "monospace", "bg": "#FFFFFF", "fg": "#000000"}

import sys
import re
from pathlib import Path

DIRIME_ROOT = Path(__file__).parent.parent
CHCL_PATH = DIRIME_ROOT / "CHCL_BASE.txt"
IMV_DIR = DIRIME_ROOT / "IMV"

def parse_chcl(chcl_path: Path) -> dict:
    """Parsea CHCL_BASE.txt y extrae divisiones y sentencias."""
    divisions = {}
    current_div = None
    current_section = None

    for line in chcl_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # DIVISION
        if "DIVISION" in stripped and stripped.endswith("."):
            current_div = stripped.rstrip(".")
            divisions[current_div] = {"sections": {}, "statements": []}
            current_section = None
            continue

        # SECTION
        if stripped.endswith("SECTION."):
            current_section = stripped.rstrip(".")
            if current_div and current_section:
                divisions[current_div]["sections"][current_section] = []
            continue

        # 01 level items
        if stripped.startswith("01 ") and current_div:
            item = stripped.lstrip("01 ").rstrip(".")
            divisions[current_div]["statements"].append(item)
            continue

        # PERFORM / CALL statements
        if stripped.startswith(("PERFORM ", "CALL ", "EXECUTE ")):
            if current_div:
                divisions[current_div]["statements"].append(stripped)

    return divisions

def validate_chcl(chcl_path: Path) -> list:
    """Valida sentencias CHCL contra grammar LACHO."""
    errors = []
    sys.path.insert(0, str(IMV_DIR))
    try:
        from core.grammar import validate
        from core.grammar import ValidationResult
    except ImportError:
        return [{"error": "IMV/core/grammar no disponible"}]

    # Extraer sentencias LACHO del CHCL (líneas con =><=)
    lacho_sentences = []
    for line in chcl_path.read_text(encoding="utf-8").splitlines():
        if "=><=".replace(" ", "") in line and "[term]" in line:
            lacho_sentences.append(line.strip())

    results = []
    for sent in lacho_sentences:
        parsed = validate(sent)
        results.append({
            "sentence": sent[:60],
            "result": parsed.result.value,
            "errors": parsed.errors
        })
    return results

def run_chcl(chcl_path: Path, mode: str = "validate", verbose: bool = False) -> dict:
    """Ejecuta CHCL según el modo especificado."""
    if not chcl_path.exists():
        return {"error": f"CHCL_BASE.txt no encontrado: {chcl_path}"}

    print(f"\n⊗ CHCL Runner · mode={mode}")
    print(f"  CEO de LACHO · {chcl_path.name}")

    if mode == "parse":
        divisions = parse_chcl(chcl_path)
        print(f"\n  Divisiones encontradas: {len(divisions)}")
        for div, content in divisions.items():
            stmts = len(content.get("statements", []))
            sects = len(content.get("sections", {}))
            print(f"    {div}: {stmts} statements · {sects} sections")
            if verbose:
                for s in content.get("statements", [])[:3]:
                    print(f"      → {s[:60]}")
        return {"mode": "parse", "divisions": list(divisions.keys())}

    elif mode == "validate":
        results = validate_chcl(chcl_path)
        valid = sum(1 for r in results if r.get("result") == "VALID")
        warn = sum(1 for r in results if r.get("result") == "WARNING")
        invalid = sum(1 for r in results if r.get("result") == "INVALID")
        print(f"\n  Sentencias LACHO en CHCL: {len(results)}")
        print(f"  VALID={valid} · WARNING={warn} · INVALID={invalid}")
        if verbose:
            for r in results:
                status = r.get("result", "?")
                icon = "✅" if status == "VALID" else "⚠️" if status == "WARNING" else "❌"
                print(f"  {icon} {r['sentence']}")
        return {"mode": "validate", "valid": valid, "warning": warn, "invalid": invalid}

    elif mode == "stats":
        lines = chcl_path.read_text(encoding="utf-8").splitlines()
        divisions = [l for l in lines if "DIVISION" in l and l.strip().endswith(".")]
        lacho = [l for l in lines if "=><=".replace(" ", "") in l and "[term]" in l]
        print(f"\n  Líneas totales:    {len(lines)}")
        print(f"  DIVISIONS:         {len(divisions)}")
        print(f"  Sentencias LACHO:  {len(lacho)}")
        return {"mode": "stats", "lines": len(lines), "divisions": len(divisions),
                "lacho_sentences": len(lacho)}

    return {"error": f"Modo desconocido: {mode}"}

def main():
    import argparse
    parser = argparse.ArgumentParser(description="CHCL Runner soberano")
    parser.add_argument("mode", nargs="?", default="validate",
                        choices=["parse", "validate", "stats"],
                        help="Modo de ejecución (default: validate)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Output detallado")
    parser.add_argument("--chcl", default=str(CHCL_PATH),
                        help="Path al archivo CHCL (default: CHCL_BASE.txt)")
    args = parser.parse_args()

    chcl_file = Path(args.chcl)
    result = run_chcl(chcl_file, args.mode, args.verbose)
    if "error" in result:
        print(f"\n  ERROR: {result['error']}")
        sys.exit(1)
    print(f"\n  ✅ CHCL Runner completado · mode={result['mode']}")

if __name__ == "__main__":
    main()
