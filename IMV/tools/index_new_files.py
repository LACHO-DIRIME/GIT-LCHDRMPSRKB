#!/usr/bin/env python3
"""
index_new_files.py — CORREGIDO $wed 2026-03-11
Indexa CORPUS + THEATER · LACHO_FILES · AGENTS · RUNNERS · ELPULSAR LOCAL al RAG
Rutas reales: RUNTIME/ · crea directorios si no existen
"""
import sys
import os
from pathlib import Path

# ── BASE REAL ─────────────────────────────────────────────────
# __file__ = /media/Personal/PLANERAI/DIRIME/IMV/tools/index_new_files.py
# parent        = tools/
# parent.parent = IMV/
# parent.parent.parent = DIRIME/   ← BASE

_TOOLS_DIR  = Path(__file__).resolve().parent
_IMV_DIR    = _TOOLS_DIR.parent
_BASE       = _IMV_DIR.parent          # /media/Personal/PLANERAI/DIRIME/
_CORPUS_DIR = _BASE / "CORPUS"
_SOVEREIGN  = _BASE / "RUNTIME"

# ── DIRECTORIOS SOBERANOS ─────────────────────────────────────
SOVEREIGN_DIRS = {
    "THEATER":       (_SOVEREIGN / "THEATER",        ["*.theater", "*.gate", "*.txt"]),
    "LACHO_FILES":   (_SOVEREIGN / "LACHO_FILES",    ["*.lacho", "*.txt"]),
    "AGENTS":        (_SOVEREIGN / "AGENTS",         ["*"]),
    "RUNNERS":       (_SOVEREIGN / "RUNNERS",        ["*.runner", "*.door", "*.txt"]),
    "ELPULSAR_LOCAL":(_SOVEREIGN / "ELPULSAR LOCAL", ["*.txt", "*.TXT"]),
    "CORPUS":        (_CORPUS_DIR,                   ["*.txt", "*.TXT"]),
}


def ensure_dirs():
    """Crea directorios soberanos si no existen."""
    for name, (path, _) in SOVEREIGN_DIRS.items():
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Creado: {path}")


def count_and_verify():
    """Cuenta archivos y verifica estado."""
    print(f"  📍 BASE:    {_BASE}")
    print(f"  📍 IMV:     {_IMV_DIR}")
    print(f"  📍 SOVRN:   {_SOVEREIGN}")
    print()
    total = 0
    for name, (path, patterns) in SOVEREIGN_DIRS.items():
        if not path.exists():
            print(f"  ⚠️  {name}: no existe → {path}")
            continue
        files = []
        for pat in patterns:
            files.extend(path.glob(pat))
        # dedup por nombre
        files = list({f.name: f for f in files if f.is_file()}.values())
        count = len(files)
        total += count
        if count > 0:
            print(f"  📁 {name}: {count} archivos  ({path})")
            for f in sorted(files)[:5]:
                print(f"       · {f.name}")
            if count > 5:
                print(f"       ... y {count - 5} más")
        else:
            print(f"  📂 {name}: vacío  ({path})")
    return total


def trigger_rag_rebuild():
    """Llama a build_full_index() del RAG para reindexar todo."""
    try:
        sys.path.insert(0, str(_IMV_DIR))
        from core.rag import build_full_index
        print("\n  🔄 Rebuilding RAG index...")
        corpus_n, behavioral_n = build_full_index()
        print(f"  ✅ RAG: {corpus_n} corpus docs · {behavioral_n} behavioral docs")
        return corpus_n
    except ImportError as e:
        print(f"  ⚠️  RAG import error: {e}")
        print(f"  💡 Ejecutar desde: {_IMV_DIR}")
        return 0
    except Exception as e:
        print(f"  ⚠️  RAG error: {e}")
        return 0


def add_corpus_unicode(filename: str, content: str):
    """Helper: agrega un archivo UNICODE al CORPUS directamente."""
    target = _CORPUS_DIR / filename
    target.write_text(content, encoding="utf-8")
    print(f"  ✅ Corpus add: {filename}")

def detect_notaria_files():
    """Detecta archivos NOTARIA específicos para indexación."""
    notaria_files = []
    
    # CORPUS/UNICODE PROGRAMS/UNICODE_NOTARIA*.txt
    corpus_notaria = list(_CORPUS_DIR.glob("UNICODE PROGRAMS/UNICODE_NOTARIA*.txt"))
    notaria_files.extend(corpus_notaria)
    
    # RUNTIME/NERVE_CELLS/$tue.Nerve Cell Notaria*.txt
    elpulsar_notaria = list((_SOVEREIGN / "ELPULSAR LOCAL").glob("$tue.Nerve Cell Notaria*.txt"))
    notaria_files.extend(elpulsar_notaria)
    
    if notaria_files:
        print(f"  🔍 Archivos NOTARIA detectados: {len(notaria_files)}")
        for f in notaria_files:
            print(f"    · {f.relative_to(_BASE)}")
    
    return notaria_files


if __name__ == "__main__":
    print("=== INDEX NEW SOVEREIGN FILES ===")
    print()

    # 1. Crear directorios faltantes
    ensure_dirs()

    # 2. Contar y verificar
    total = count_and_verify()
    
    # 2.1 Detectar archivos NOTARIA
    notaria_files = detect_notaria_files()
    
    print(f"\n  Total archivos soberanos encontrados: {total}")
    if notaria_files:
        print(f"  Incluyendo {len(notaria_files)} archivos NOTARIA con boost")

    # 3. Rebuild RAG si hay --rag flag o si hay archivos
    rebuild = "--rag" in sys.argv or "--all" in sys.argv or total > 0
    if rebuild:
        n = trigger_rag_rebuild()
        if n > 0:
            print(f"\n  ✅ Indexación completa · {n} docs en RAG")
        else:
            print(f"\n  ⚠️  RAG rebuild falló · verificar rutas")
    else:
        print("\n  💡 Usar --rag para forzar rebuild del RAG")
        print(f"  💡 Ejemplo: python3 {Path(__file__).name} --rag")

    print()
    print(f"  BASE:   {_BASE}")
    print(f"  CORPUS: {_CORPUS_DIR} ({len(list(_CORPUS_DIR.rglob('*.txt')))} .txt vía rglob)")
    sys.exit(0)
