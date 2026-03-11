"""
IMV/tools/export_crystals_lacho.py
Exporta cristales del ledger como sentencias LACHO verificadas.
Referencia: BIBLIO-SOURCES(DIRIME-IMV_LEDGER).txt §5.0
"""
from __future__ import annotations
import sys, json, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.ledger import export_crystals_report

def export_lacho(output_path: str = None) -> dict:
    """
    Exporta cristales como archivo LACHO-readable.
    Formato: una sentencia canónica por cristal.
    """
    report = export_crystals_report()
    crystals = report.get("crystals", [])

    lines = [
        "# EXPORT CRISTALES LACHO",
        f"# timestamp: {time.strftime('%Y-%m-%d %H:%M')}",
        f"# total: {len(crystals)}",
        "",
    ]

    for c in crystals:
        form   = c.get("form", "")
        freq   = c.get("frequency", 0)
        lib    = c.get("library", "METHOD")
        tomo   = c.get("tomo_id", "[term]")
        lines.append(
            f"STACKING UF[H52] =><= .. inmutabiliza .. {form} "
            f"--[Nudo de Ocho] {tomo}  # freq={freq} lib={lib}"
        )

    content = "\n".join(lines)

    if output_path is None:
        output_path = str(Path(__file__).parent.parent /
                          "data" / "crystals_export.lacho")

    Path(output_path).write_text(content, encoding="utf-8")
    return {
        "exported": len(crystals),
        "path": output_path,
        "timestamp": time.time()
    }

if __name__ == "__main__":
    result = export_lacho()
    print(f"✅ {result['exported']} cristales → {result['path']}")
