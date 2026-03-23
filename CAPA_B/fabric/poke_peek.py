"""
DIRIME_v2 — fabric/poke_peek.py
POKE+TRUST / PEEK+CRYPTO — forma mínima con SQLite.

Referencia: BIBLIO-SOURCES(OPERACIONES-ESPECIALES).txt §4 y §5
Forma completa futura: Hyperledger Fabric Invoke/GetState.

POKE = escritura soberana — solo si verify_sovereign_conditions() pasa
PEEK = consulta aislada en sandbox — read-only, sin contaminar núcleo
"""

from __future__ import annotations
import sqlite3
import json
import time
import uuid
from pathlib import Path
from typing import Any, Optional

# Ruta al ledger soberano IMV
_IMV_DB = Path(__file__).parent.parent.parent / "IMV" / "data" / "sovereign.db"


# ── POKE — escritura soberana ─────────────────────────────────────

def poke(
    key: str,
    value: Any,
    tomo_id: Optional[str] = None,
    cluster: Optional[str] = None,
    require_sovereign: bool = True
) -> dict:
    """
    POKE + TRUST — escritura soberana verificada.

    Solo ejecuta si las condiciones soberanas se cumplen.
    Registra la operación como transacción inmutable.

    Args:
        key: identificador soberano del dato
        value: valor a escribir (será serializado a JSON)
        tomo_id: referencia TOMO opcional [term:X]
        cluster: cluster temático opcional #NOMBRE
        require_sovereign: si True, verifica condiciones antes de escribir

    Returns:
        dict con id, key, tomo_id, timestamp, status
    """
    # Verificación soberana TRUST
    if require_sovereign:
        _verify_poke_conditions(key, value)

    tx_id = str(uuid.uuid4())
    ts = time.time()

    with sqlite3.connect(_IMV_DB) as conn:
        # Crear tabla fabric si no existe
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fabric_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                tomo_id TEXT,
                cluster TEXT,
                tx_id TEXT NOT NULL,
                timestamp REAL NOT NULL,
                operation TEXT DEFAULT 'POKE'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fabric_log (
                id TEXT PRIMARY KEY,
                operation TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT,
                tomo_id TEXT,
                cluster TEXT,
                timestamp REAL NOT NULL,
                status TEXT DEFAULT 'OK'
            )
        """)

        # Escribir estado soberano
        conn.execute("""
            INSERT OR REPLACE INTO fabric_state
            (key, value, tomo_id, cluster, tx_id, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (key, json.dumps(value), tomo_id, cluster, tx_id, ts))

        # Registrar en log inmutable
        conn.execute("""
            INSERT INTO fabric_log
            (id, operation, key, value, tomo_id, cluster, timestamp, status)
            VALUES (?, 'POKE', ?, ?, ?, ?, ?, 'OK')
        """, (tx_id, key, json.dumps(value)[:500], tomo_id, cluster, ts))

        conn.commit()

    return {
        "id": tx_id,
        "operation": "POKE",
        "key": key,
        "tomo_id": tomo_id,
        "cluster": cluster,
        "timestamp": ts,
        "status": "OK"
    }


def _verify_poke_conditions(key: str, value: Any) -> None:
    """
    Verificación soberana TRUST antes de POKE.
    Lanza SovereignPokeError si las condiciones no se cumplen.
    """
    if not key or not isinstance(key, str):
        raise SovereignPokeError("POKE rechazado: key inválida")
    if key.startswith("_"):
        raise SovereignPokeError(f"POKE rechazado: key '{key}' reservada al sistema")
    if value is None:
        raise SovereignPokeError("POKE rechazado: value None no es soberano")
    try:
        json.dumps(value)
    except (TypeError, ValueError) as e:
        raise SovereignPokeError(f"POKE rechazado: value no serializable — {e}")


# ── PEEK — consulta aislada en sandbox ───────────────────────────

def peek(
    key: str,
    tomo_id: Optional[str] = None
) -> Optional[Any]:
    """
    PEEK + CRYPTO — consulta aislada en sandbox read-only.

    Lee sin contaminar el núcleo soberano.
    El sandbox se destruye después de retornar el dato.

    Args:
        key: identificador soberano del dato a leer
        tomo_id: filtro TOMO opcional

    Returns:
        valor deserializado, o None si no existe
    """
    tx_id = str(uuid.uuid4())
    ts = time.time()
    result = None

    # Sandbox: conexión read-only aislada
    try:
        conn = sqlite3.connect(f"file:{_IMV_DB}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            if tomo_id:
                row = conn.execute(
                    "SELECT value FROM fabric_state WHERE key = ? AND tomo_id = ?",
                    (key, tomo_id)
                ).fetchone()
            else:
                row = conn.execute(
                    "SELECT value FROM fabric_state WHERE key = ?",
                    (key,)
                ).fetchone()

            if row:
                result = json.loads(row["value"])
        finally:
            conn.close()  # sandbox destruido aquí
    except Exception:
        result = None

    # Registrar PEEK en log (conexión separada, read-write)
    try:
        with sqlite3.connect(_IMV_DB) as log_conn:
            log_conn.execute("""
                CREATE TABLE IF NOT EXISTS fabric_log (
                    id TEXT PRIMARY KEY,
                    operation TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT,
                    tomo_id TEXT,
                    cluster TEXT,
                    timestamp REAL NOT NULL,
                    status TEXT DEFAULT 'OK'
                )
            """)
            log_conn.execute("""
                INSERT INTO fabric_log
                (id, operation, key, tomo_id, timestamp, status)
                VALUES (?, 'PEEK', ?, ?, ?, ?)
            """, (tx_id, key, tomo_id, ts, 'OK' if result is not None else 'NOT_FOUND'))
            log_conn.commit()
    except Exception:
        pass

    return result


def peek_all(cluster: Optional[str] = None) -> dict:
    """
    PEEK de todo el estado fabric, opcionalmente filtrado por cluster.
    Read-only sandbox completo.
    """
    result = {}
    try:
        conn = sqlite3.connect(f"file:{_IMV_DB}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
        try:
            if cluster:
                rows = conn.execute(
                    "SELECT key, value, tomo_id FROM fabric_state WHERE cluster = ?",
                    (cluster,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT key, value, tomo_id FROM fabric_state"
                ).fetchall()
            for row in rows:
                result[row["key"]] = {
                    "value": json.loads(row["value"]),
                    "tomo_id": row["tomo_id"]
                }
        finally:
            conn.close()
    except Exception:
        pass
    return result


def fabric_log(limit: int = 20) -> list[dict]:
    """Retorna el log soberano de operaciones POKE/PEEK."""
    try:
        with sqlite3.connect(_IMV_DB) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM fabric_log
                ORDER BY timestamp DESC LIMIT ?
            """, (limit,)).fetchall()
            return [dict(r) for r in rows]
    except Exception:
        return []


# ── Excepción soberana ───────────────────────────────────────────

class SovereignPokeError(Exception):
    """Error soberano: POKE rechazado por condiciones TRUST."""
    pass


# ── Test soberano ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("POKE + PEEK — test soberano")
    print("=" * 50)

    # POKE test
    r = poke("test_key", {"valor": "soberano"}, tomo_id="term:A", cluster="#CORE")
    print(f"POKE: {r['status']} — id: {r['id'][:8]}...")

    # PEEK test
    v = peek("test_key")
    print(f"PEEK: {v}")

    # PEEK con tomo_id
    v2 = peek("test_key", tomo_id="term:A")
    print(f"PEEK tomo: {v2}")

    # PEEK inexistente
    v3 = peek("no_existe")
    print(f"PEEK vacío: {v3}")

    # peek_all
    all_state = peek_all(cluster="#CORE")
    print(f"PEEK_ALL #CORE: {len(all_state)} entradas")

    # log
    log = fabric_log(5)
    print(f"LOG: {len(log)} entradas recientes")
    print("=" * 50)
