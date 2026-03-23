"""
DIRIME_v2 — scheduler/scheduler.py
Scheduler OS soberano — ciclo semanal con TOMO/SLICE/CLUSTER.

Referencia: BIBLIO-SOURCES(SOCIAL_SCHEDULER-OS).txt
            BIBLIO-SOURCES(SEGMENTACION-SOBERANA).txt
Python puro — sin dependencias externas.
"""

from __future__ import annotations
import json
import time
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Optional
from enum import Enum

_IMV_DIR  = Path(__file__).parent.parent.parent / "IMV"
_IMV_DB   = _IMV_DIR / "data" / "sovereign.db"
_SCHED_DB = Path(__file__).parent / "scheduler.db"


# ── Días soberanos ───────────────────────────────────────────────

class DiaSoberano(Enum):
    MON = "$mon"
    TUE = "$tue"
    WED = "$wed"
    THU = "$thu"
    FRI = "$fri"
    SAT = "$sat"
    SUN = "$sun"

    @classmethod
    def hoy(cls) -> "DiaSoberano":
        dias = [cls.MON, cls.TUE, cls.WED, cls.THU,
                cls.FRI, cls.SAT, cls.SUN]
        return dias[datetime.now().weekday()]


# ── Estado de tarea ──────────────────────────────────────────────

class EstadoTarea(Enum):
    ESPERA     = "UF[H05]"   # Gate — esperando
    ACTIVA     = "UF[H57]"   # Activity — penetrante
    RESUELTA   = "UF[H63]"   # Después del fin
    CONFLICTO  = "UF[H06]"   # Gate — conflicto


# ── Tarea soberana ───────────────────────────────────────────────

class TareaSoberana:
    def __init__(
        self,
        titulo: str,
        dia: DiaSoberano,
        cluster: str = "#CORE",
        slice_grados: int = 90,
        tomo_id: Optional[str] = None,
        segment: Optional[str] = None,
    ):
        self.id = str(uuid.uuid4())[:8]
        self.titulo = titulo
        self.dia = dia
        self.cluster = cluster
        self.slice_grados = slice_grados
        self.tomo_id = tomo_id
        self.segment = segment
        self.estado = EstadoTarea.ESPERA
        self.created_at = time.time()

    def ref_soberana(self) -> str:
        """Retorna referencia canónica [term:X°N#CLUSTER§R]"""
        parts = []
        if self.tomo_id:
            parts.append(self.tomo_id.replace("term:", ""))
        parts_str = "".join(parts) or "?"
        ref = f"[term:{parts_str}°{self.slice_grados}"
        if self.segment:
            ref += f"§{self.segment}"
        ref += f"{self.cluster}]"
        return ref

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "dia": self.dia.value,
            "cluster": self.cluster,
            "slice_grados": self.slice_grados,
            "tomo_id": self.tomo_id,
            "segment": self.segment,
            "estado": self.estado.value,
            "ref": self.ref_soberana(),
            "created_at": self.created_at,
        }


# ── Scheduler OS soberano ────────────────────────────────────────

class SchedulerOS:
    """
    Sistema Operativo de Ciclos Soberanos.
    Planifica decisiones soberanas, no procesos de CPU.
    """

    def __init__(self):
        self._init_db()

    def _init_db(self):
        with __import__('sqlite3').connect(_SCHED_DB) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tareas (
                    id TEXT PRIMARY KEY,
                    titulo TEXT NOT NULL,
                    dia TEXT NOT NULL,
                    cluster TEXT,
                    slice_grados INTEGER DEFAULT 90,
                    tomo_id TEXT,
                    segment TEXT,
                    estado TEXT DEFAULT 'UF[H05]',
                    created_at REAL,
                    updated_at REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ciclos (
                    id TEXT PRIMARY KEY,
                    semana TEXT NOT NULL,
                    dia TEXT NOT NULL,
                    evento TEXT NOT NULL,
                    timestamp REAL NOT NULL
                )
            """)
            conn.commit()

    def planifica(
        self,
        titulo: str,
        dia: Optional[DiaSoberano] = None,
        cluster: str = "#CORE",
        slice_grados: int = 90,
        tomo_id: Optional[str] = None,
        segment: Optional[str] = None,
    ) -> TareaSoberana:
        """
        SOCIAL {scheduler} =><= .. planifica .. tarea_soberana
        Registra una tarea en el ciclo semanal.
        """
        if dia is None:
            dia = DiaSoberano.hoy()

        tarea = TareaSoberana(
            titulo=titulo,
            dia=dia,
            cluster=cluster,
            slice_grados=slice_grados,
            tomo_id=tomo_id,
            segment=segment,
        )

        import sqlite3
        with sqlite3.connect(_SCHED_DB) as conn:
            conn.execute("""
                INSERT INTO tareas
                (id, titulo, dia, cluster, slice_grados, tomo_id,
                 segment, estado, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tarea.id, tarea.titulo, tarea.dia.value,
                tarea.cluster, tarea.slice_grados,
                tarea.tomo_id, tarea.segment,
                tarea.estado.value, tarea.created_at, tarea.created_at
            ))
            conn.commit()

        self._registrar_ciclo(tarea.dia, f"PLANIFICA:{tarea.titulo[:40]}")
        return tarea

    def activar(self, tarea_id: str) -> bool:
        """Activa una tarea — UF[H05]→UF[H57]."""
        import sqlite3
        with sqlite3.connect(_SCHED_DB) as conn:
            n = conn.execute("""
                UPDATE tareas SET estado = ?, updated_at = ?
                WHERE id = ? AND estado = ?
            """, (
                EstadoTarea.ACTIVA.value, time.time(),
                tarea_id, EstadoTarea.ESPERA.value
            )).rowcount
            conn.commit()
        return n > 0

    def resolver(self, tarea_id: str) -> bool:
        """Resuelve una tarea — UF[H57]→UF[H63]."""
        import sqlite3
        with sqlite3.connect(_SCHED_DB) as conn:
            n = conn.execute("""
                UPDATE tareas SET estado = ?, updated_at = ?
                WHERE id = ?
            """, (EstadoTarea.RESUELTA.value, time.time(), tarea_id)).rowcount
            conn.commit()
        return n > 0

    def tareas_del_dia(
        self,
        dia: Optional[DiaSoberano] = None,
        cluster: Optional[str] = None
    ) -> list[dict]:
        """Retorna tareas del día, opcionalmente filtradas por cluster."""
        if dia is None:
            dia = DiaSoberano.hoy()
        import sqlite3
        with sqlite3.connect(_SCHED_DB) as conn:
            conn.row_factory = sqlite3.Row
            if cluster:
                rows = conn.execute("""
                    SELECT * FROM tareas
                    WHERE dia = ? AND cluster = ?
                    ORDER BY slice_grados ASC
                """, (dia.value, cluster)).fetchall()
            else:
                rows = conn.execute("""
                    SELECT * FROM tareas WHERE dia = ?
                    ORDER BY slice_grados ASC
                """, (dia.value,)).fetchall()
        return [dict(r) for r in rows]

    def estado_semana(self) -> dict:
        """Estado completo de la semana soberana."""
        import sqlite3
        semana = {}
        with sqlite3.connect(_SCHED_DB) as conn:
            conn.row_factory = sqlite3.Row
            for dia in DiaSoberano:
                rows = conn.execute(
                    "SELECT * FROM tareas WHERE dia = ? ORDER BY slice_grados",
                    (dia.value,)
                ).fetchall()
                semana[dia.value] = {
                    "tareas": [dict(r) for r in rows],
                    "total": len(rows),
                    "resueltas": sum(
                        1 for r in rows
                        if r["estado"] == EstadoTarea.RESUELTA.value
                    )
                }
        return semana

    def _registrar_ciclo(self, dia: DiaSoberano, evento: str):
        """Registra evento en el log de ciclos soberanos."""
        import sqlite3
        semana = date.today().strftime("%Y-W%W")
        with sqlite3.connect(_SCHED_DB) as conn:
            conn.execute("""
                INSERT INTO ciclos (id, semana, dia, evento, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (str(uuid.uuid4())[:8], semana, dia.value, evento, time.time()))
            conn.commit()

    def rise(self, dia: Optional[DiaSoberano] = None) -> str:
        """
        SAMU #rise =><= .. activa .. periodo_soberano
        Abre el período soberano del día.
        """
        if dia is None:
            dia = DiaSoberano.hoy()
        self._registrar_ciclo(dia, f"#rise — periodo abierto")
        return f"#rise activo — {dia.value} — periodo soberano abierto"

    def set(self, dia: Optional[DiaSoberano] = None) -> str:
        """
        SAMU #set =><= .. cierra .. periodo_soberano
        Cierra el período soberano del día.
        """
        if dia is None:
            dia = DiaSoberano.hoy()
        self._registrar_ciclo(dia, f"#set — periodo cerrado")
        tareas = self.tareas_del_dia(dia)
        resueltas = sum(1 for t in tareas if t["estado"] == EstadoTarea.RESUELTA.value)
        return (
            f"#set activo — {dia.value} — periodo soberano cerrado\n"
            f"  {resueltas}/{len(tareas)} tareas resueltas"
        )


# ── Instancia global ─────────────────────────────────────────────
_scheduler = SchedulerOS()

def planifica(titulo: str, **kwargs) -> TareaSoberana:
    return _scheduler.planifica(titulo, **kwargs)

def rise(dia=None) -> str:
    return _scheduler.rise(dia)

def set_dia(dia=None) -> str:
    return _scheduler.set(dia)

def estado_semana() -> dict:
    return _scheduler.estado_semana()


# ── Test soberano ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("SCHEDULER OS — test soberano")
    print("=" * 50)

    # Rise
    print(rise())

    # Planificar tareas
    t1 = planifica(
        "Verificar ledger soberano",
        dia=DiaSoberano.MON,
        cluster="#CORE",
        slice_grados=90,
        tomo_id="term:A"
    )
    print(f"Tarea: {t1.titulo} — {t1.ref_soberana()}")

    t2 = planifica(
        "Evaluar ciclo memecoins",
        dia=DiaSoberano.MON,
        cluster="#MERCADO",
        slice_grados=180,
        tomo_id="term:BC"
    )
    print(f"Tarea: {t2.titulo} — {t2.ref_soberana()}")

    # Activar y resolver
    _scheduler.activar(t1.id)
    _scheduler.resolver(t1.id)

    # Estado del día
    tareas = _scheduler.tareas_del_dia(DiaSoberano.MON)
    print(f"Tareas $mon: {len(tareas)}")
    for t in tareas:
        print(f"  {t['estado']} {t['titulo']} {t.get('cluster','')}")

    # Set
    print(set_dia())

    print("=" * 50)
