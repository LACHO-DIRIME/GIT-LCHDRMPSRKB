#!/usr/bin/env python3
"""
tools/theater_runner.py — Ejecutor soberano de archivos .theater
Parsea CMD_* de rational_day.theater y los ejecuta
[term] :: activo · [seal of secrecy] :: activo
"""

STYLE = {"font": "monospace", "bg": "#FFFFFF", "fg": "#000000"}

import sys
import re
import subprocess
from pathlib import Path

THEATER_DIR = Path(__file__).parent.parent / "FOLDERS NO RAG INPUT" / "THEATER"
IMV_DIR = Path(__file__).parent.parent / "IMV"

VALID_MACROS = ["macro_temprano", "macro_tarde", "macro_cierre"]

def parse_theater(theater_path: Path) -> dict:
    """Parsea un archivo .theater y extrae CMDs por macro."""
    macros = {}
    current_macro = None
    in_block = False

    for line in theater_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        # Detectar inicio de macro
        for macro in VALID_MACROS:
            if stripped.startswith(macro) and "{" in stripped:
                current_macro = macro
                in_block = True
                macros[current_macro] = []
                break

        # Detectar cierre de bloque
        if stripped == "}" and in_block:
            in_block = False
            current_macro = None
            continue

        # Extraer CMD_* dentro del bloque
        if in_block and current_macro and stripped.startswith("# CMD_"):
            # Formato: # CMD_NOMBRE: comando
            match = re.match(r"#\s*CMD_(\w+):\s*(.+)", stripped)
            if match:
                cmd_name = match.group(1)
                cmd_body = match.group(2).strip()
                macros[current_macro].append({
                    "name": cmd_name,
                    "cmd": cmd_body
                })

    return macros

def run_macro(macro_name: str, theater_file: str = "rational_day.theater",
              dry_run: bool = False) -> dict:
    """Ejecuta todos los CMD_* de un macro específico."""
    theater_path = THEATER_DIR / theater_file
    if not theater_path.exists():
        return {"error": f"Theater no encontrado: {theater_path}"}

    macros = parse_theater(theater_path)

    if macro_name not in macros:
        return {"error": f"Macro '{macro_name}' no encontrado en {theater_file}"}

    cmds = macros[macro_name]
    results = []

    for entry in cmds:
        cmd = entry["cmd"]
        print(f"  → CMD_{entry['name']}: {cmd}")

        if dry_run:
            results.append({"cmd": entry["name"], "status": "dry_run", "output": cmd})
            continue

        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=60, cwd=str(IMV_DIR)
            )
            status = "ok" if result.returncode == 0 else "error"
            output = result.stdout.strip() or result.stderr.strip()
            print(f"     {status.upper()}: {output[:80]}")
            results.append({"cmd": entry["name"], "status": status, "output": output})
        except subprocess.TimeoutExpired:
            results.append({"cmd": entry["name"], "status": "timeout", "output": ""})
        except Exception as e:
            results.append({"cmd": entry["name"], "status": "error", "output": str(e)})

    return {"macro": macro_name, "results": results, "total": len(results)}

def list_macros(theater_file: str = "rational_day.theater") -> None:
    """Lista macros y CMDs disponibles."""
    theater_path = THEATER_DIR / theater_file
    if not theater_path.exists():
        print(f"Theater no encontrado: {theater_path}")
        return

    macros = parse_theater(theater_path)
    print(f"\nTheater: {theater_file}")
    for macro, cmds in macros.items():
        print(f"  {macro}: {len(cmds)} CMD(s)")
        for c in cmds:
            print(f"    CMD_{c['name']}: {c['cmd'][:60]}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Theater Runner soberano")
    parser.add_argument("macro", nargs="?",
                        choices=VALID_MACROS + ["list"],
                        help="Macro a ejecutar o 'list' para ver disponibles")
    parser.add_argument("--theater", default="rational_day.theater",
                        help="Archivo .theater (default: rational_day.theater)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Mostrar CMDs sin ejecutar")
    args = parser.parse_args()

    if not args.macro or args.macro == "list":
        list_macros(args.theater)
        return

    print(f"\n⊗ Theater Runner · {args.macro} · {args.theater}")
    result = run_macro(args.macro, args.theater, args.dry_run)

    if "error" in result:
        print(f"  ERROR: {result['error']}")
        sys.exit(1)

    ok = sum(1 for r in result["results"] if r["status"] in ("ok", "dry_run"))
    print(f"\n  ✅ {ok}/{result['total']} CMDs completados")

if __name__ == "__main__":
    main()
