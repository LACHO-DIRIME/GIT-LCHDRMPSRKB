# Scheduler.door$wed.py
# SCHEDULER SOBERANO · $wed H58+H59 · Lo Gozoso + La Dispersión
# Energía: creatividad · diseño · UNICODE · flujo pleno
# [term] :: activo

import sqlite3
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
DB = BASE / "$wed.march.2026.db"

SCHEDULE_WED = [
    ("06:00", "ZIP_OPEN", "FEED_0600 · leer reporte bots · SAMU @", "high"),
    ("07:00", "WORK_KU", "tarea principal $wed · UNICODE · diseño", "high"),
    ("09:00", "CHECK", "python3 main.py --stats · verificar S", "medium"),
    ("12:00", "ZIPPER_NOON", "TARDANZA DELIBERADA · pausa soberana", "high"),
    ("13:00", "AFTERNOON", "DOOR AFTERNOON · WU materializable", "high"),
    ("15:00", "STACKING", "cristalizar WU del día · export_crystals", "medium"),
    ("17:00", "GIT_SYNC", "github_sync.sh · main sellado", "high"),
    ("17:45", "CIERRE", "macro_cierre · notas · SESION_ACTIVA.md", "high"),
    ("18:00", "ZIP_CLOSE", "FEED_1800 · bots toman relevo nocturno", "high"),
]

HEXAGRAMA = "H58+H59"
DIA = "$wed"

def registrar_sesion(scalar_s: float, tx_count: int, notas: str = ""):
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO sessions (fecha, dia, hexagrama, scalar_s, tx_count, notas) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), DIA, HEXAGRAMA, scalar_s, tx_count, notas)
    )
    conn.commit()
    conn.close()
    print(f"✅ Sesión {DIA} registrada · S={scalar_s} · TX={tx_count}")

def mostrar_schedule():
    print(f"\n{'='*50}")
    print(f"SCHEDULER {DIA} · {HEXAGRAMA} · Lo Gozoso")
    print(f"{'='*50}")
    now = datetime.now().strftime("%H:%M")
    for hora, nombre, desc, prio in SCHEDULE_WED:
        marker = "→" if hora <= now else " "
        print(f"{marker} {hora} [{prio.upper()[:3]}] {nombre}")
        print(f"       {desc}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    mostrar_schedule()
