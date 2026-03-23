# Scheduler.door$fri.py
# SCHEDULER SOBERANO · $fri H62+H63 · Ajuste + Consumación
# Energía: revisión final · cristalización semanal · WU del ciclo
# [term] :: activo

import sqlite3
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
DB = BASE / "$fri.march.2026.db"

SCHEDULE_FRI = [
    ("06:00", "ZIP_OPEN",    "FEED_0600 · revisar semana · #rise",           "high"),
    ("07:00", "REVIEW",      "BALLPAPER revisión semanal · estado_semana()", "high"),
    ("08:30", "STACKING_W",  "cristales semana · H63 consumación",           "high"),
    ("09:00", "CHECK",       "python3 main.py --stats · S semana final",     "medium"),
    ("11:00", "KALIL_REV",   "NORA SCHED_REVIEW · TANDIL consolidación",    "medium"),
    ("12:00", "ZIPPER_NOON", "TARDANZA DELIBERADA · pausa soberana",        "high"),
    ("13:00", "AFTERNOON",   "DOOR AFTERNOON · WU semana materializable",   "high"),
    ("15:00", "BALLPAPER",   "BALLPAPER semanal · dashboard metrics",       "high"),
    ("17:00", "GIT_SYNC",    "github_sync.sh · commit soberano semanal",    "high"),
    ("17:45", "CIERRE_SEM",  "macro_cierre semana · H63 → H64 ciclo nuevo", "high"),
    ("18:00", "ZIP_CLOSE",   "BOT_NET fin semana · $sat prep",              "high"),
]

HEXAGRAMA = "H62+H63"
DIA = "$fri"

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
    print(f"SCHEDULER {DIA} · {HEXAGRAMA} · Ajuste + Consumación")
    print(f"{'='*52}")
    now = datetime.now().strftime("%H:%M")
    for hora, nombre, desc, prio in SCHEDULE_FRI:
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
