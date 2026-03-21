# Scheduler.door$thu.py
# SCHEDULER SOBERANO · $thu H60+H61 · Limitación + Verdad Interior
# Energía: definición de límites · verdad que emerge · código preciso
# [term] :: activo

import sqlite3
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
DB = BASE / "$thu.march.2026.db"

SCHEDULE_THU = [
    ("06:00", "ZIP_OPEN",    "FEED_0600 · estado semana · SAMU #rise",       "high"),
    ("07:00", "WORK_KU",     "TAREA_01 $thu · grammar ACTIVITY_H03→H06",     "high"),
    ("08:30", "WORK_KU_2",   "tests generator.py · 27→33 target",            "high"),
    ("09:00", "CHECK",       "python3 main.py --stats · verificar S · tests", "medium"),
    ("10:00", "WORK_KU_3",   "TAREA_02 $thu · TAREA_03 si hay tiempo",       "high"),
    ("12:00", "ZIPPER_NOON", "TARDANZA DELIBERADA · 空 · H61 verdad interior","high"),
    ("13:00", "AFTERNOON",   "DOOR AFTERNOON · WU materializable · @later",   "high"),
    ("15:00", "STACKING",    "cristalizar WU del día · export_crystals",      "medium"),
    ("17:00", "GIT_SYNC",    "github_sync.sh · main sellado · H60 límite",   "high"),
    ("17:45", "CIERRE",      "macro_cierre · SESION_ACTIVA.md update",        "high"),
    ("18:00", "ZIP_CLOSE",   "FEED_1800 · BOT_NET toma relevo nocturno",     "high"),
]

HEXAGRAMA = "H60+H61"
DIA = "$thu"

def registrar_sesion(scalar_s: float, tx_count: int, notas: str = ""):
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT OR IGNORE INTO sessions "
        "(fecha, dia, hexagrama, scalar_s, tx_count, notas) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), DIA, HEXAGRAMA, scalar_s, tx_count, notas)
    )
    conn.commit(); conn.close()
    print(f"✅ Sesión {DIA} registrada · S={scalar_s} · TX={tx_count}")

def mostrar_schedule():
    print(f"\n{'='*52}")
    print(f"SCHEDULER {DIA} · {HEXAGRAMA} · Limitación + Verdad")
    print(f"{'='*52}")
    now = datetime.now().strftime("%H:%M")
    for hora, nombre, desc, prio in SCHEDULE_THU:
        status = "✓" if hora <= now else " "
        print(f"{status} {hora} {nombre:12} {prio:7} · {desc}")
    print(f"{'='*52}")

def crear_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            fecha TEXT,
            dia TEXT,
            hexagrama TEXT,
            scalar_s REAL,
            tx_count INTEGER,
            notas TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            dia TEXT,
            task TEXT,
            status TEXT,
            priority TEXT
        )
    """)
    conn.commit(); conn.close()

if __name__ == "__main__":
    crear_db()
    mostrar_schedule()
