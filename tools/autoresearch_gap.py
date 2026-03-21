#!/usr/bin/env python3
"""
tools/autoresearch_gap.py — Gap detector + Groq → $dia_asks_DDMM.txt
[term] :: activo
"""

STYLE = {"font": "monospace", "bg": "#FFFFFF", "fg": "#000000"}

import sys
import json
from pathlib import Path
from datetime import datetime

REPO_ROOT   = Path(__file__).parent.parent
IMV_ROOT    = REPO_ROOT / "IMV"
ASKINGS_DIR = REPO_ROOT / "Askings for autoresearching by technical horizons"
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(IMV_ROOT))

AUTORESEARCH_SYSTEM_PROMPT = """
Eres el motor de autoresearch soberano de DIRIME/IMV.
Analizas gaps técnicos y generas tareas LACHO accionables.

REGLAS:
1. Solo tareas CAPA_B (hardware actual disponible · antiX · Groq)
2. Cada ASK = sentencia LACHO válida + prioridad + horas estimadas
3. Priorizar por impacto en Scalar S y módulos desbloqueados
4. Formato ESTRICTO — ningún texto extra fuera del bloque ASK
5. NO sugerir CAPA C (Ollama · cat_local · ime · Ryzen)

BIBLIOTECAS: TRUST · STACKING · SAMU · GATE · WORK · ACTIVITY · CRYPTO · SOCIAL · METHOD
NUDOS: [As de Guía] · [Nudo de Ocho] · [Ballestrinque] · [Nudo Corredizo]
FORMATO RESPUESTA:
ASK_{N:02d} | ALTA/MEDIA/BAJA | CAPA_B | ~{h}h
  {sentencia LACHO válida}
  impacto: {una línea}
  desbloquea: {módulos}

BLOQUEADOS (no sugerir):
  DIRIME_v3/ime/ · DIRIME_v3/cat_local/ · DIRIME_v3/ollama_bridge/
"""

def load_context_package() -> str:
    """Carga contexto comprimido para Groq · max 3000 tokens."""
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    import autoresearch_specs as specs
    modules = specs.scan_filesystem()
    db      = specs.scan_sovereign_db()
    gaps    = specs.scan_corpus_gaps()

    active   = [k for k,v in modules.items() if v["status"]=="ACTIVE"]
    pending  = [k for k,v in modules.items() if v["status"] in ("DECLARED","STUB")]

    pkg = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "tx": db.get("tx_total", 0),
        "cristales": db.get("crystals", 0),
        "scalar_s": db.get("scalar_s", "?"),
        "tests": "49/49",
        "capa_activa": "CAPA_B",
        "hardware": "antiX · Groq API",
        "activos": active[:10],
        "pendientes": pending[:8],
        "gaps": gaps[:6],
    }
    return json.dumps(pkg, ensure_ascii=False, indent=2)

def generate_asks(context: str) -> str:
    """Llama a Groq via bridge y retorna asks en formato LACHO."""
    try:
        from DIRIME_v2.groq.bridge import translate, is_active
        if not is_active():
            return _fallback_asks()
        prompt = AUTORESEARCH_SYSTEM_PROMPT.format(
            tx=0, cristales=0, scalar="?", tests="49/49"
        ) if "{tx}" in AUTORESEARCH_SYSTEM_PROMPT else AUTORESEARCH_SYSTEM_PROMPT
        result = translate(context, prompt)
        return result or _fallback_asks()
    except Exception as e:
        print(f"  ⚠ Groq no disponible: {e}")
        return _fallback_asks()

def _fallback_asks() -> str:
    return """ASK_01 | ALTA | CAPA_B | ~30min
  WORK {actuator} =><= .. implementa .. github_sync_valores_reales_tx_scalar --[As de Guía] [term]
  impacto: commit message con TX/S reales en vez de hardcodeados
  desbloquea: github_sync.sh fidelidad · log permanente correcto

ASK_02 | ALTA | CAPA_B | ~1h
  WORK {actuator} =><= .. implementa .. scalar_s_en_notaria_archivo_endpoint --[As de Guía] [term]
  impacto: scalar_s:0 → valor real en /api/notaria/archivo
  desbloquea: export_notaria_report calidad · métricas reales

ASK_03 | MEDIA | CAPA_B | ~2h
  WORK {actuator} =><= .. implementa .. theater_runner_cmd_executor --[As de Guía] [term]
  impacto: ciclo diario automatizable · macro_cierre real
  desbloquea: rational_day.theater ejecutable · github_sync automático

ASK_BLOCKED_01: DIRIME_v3/ollama_bridge/ → requiere PC Ryzen
ASK_BLOCKED_02: DIRIME_v3/ime/ → requiere Ollama local"""

def save_asks(asks_text: str) -> Path:
    """Guarda asks del día y actualiza sovereign.db via POKE."""
    fecha = datetime.now().strftime("%d-%m")
    dia   = datetime.now().strftime("%a").lower()[:3]
    fname = f"${dia}_asks_{fecha}.txt"
    header = f"""// ASKING · ${dia} {fecha} · autoresearch soberano · Groq llama-3.3-70b
// TX={0} · generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// horizonte activo: CAPA_B · hardware antiX · Groq API

"""
    path = ASKINGS_DIR / fname
    path.write_text(header + asks_text + "\n\n[term] :: activo · generado por autoresearch_gap.py\n")

    # POKE en sovereign.db
    try:
        from DIRIME_v2.fabric.poke_peek import poke
        poke("autoresearch:last_run", datetime.now().isoformat(), cluster="#ASKS")
        poke("autoresearch:last_file", str(path), cluster="#ASKS")
    except Exception:
        pass

    # Append a PENDIENTES.md
    pendientes = REPO_ROOT / "JOURNAL" / "PENDIENTES.md"
    if pendientes.exists():
        with open(pendientes, "a") as f:
            f.write(f"\n// autoresearch {fecha}: {fname} generado\n")

    return path

def main():
    print("⬡ autoresearch_gap.py · gap detector + Groq")
    print("  PASO 1 · cargar contexto...")
    context = load_context_package()
    print(f"         {len(context)} chars · context package listo")
    print("  PASO 2 · Groq translate...")
    asks = generate_asks(context)
    print(f"         {asks.count('ASK_')} asks generados")
    print("  PASO 3 · guardar...")
    path = save_asks(asks)
    print(f"\n✅ asks guardados: {path}")
    print(f"   {path}\n")
    return path

if __name__ == "__main__":
    main()
