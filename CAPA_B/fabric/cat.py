"""
DIRIME_v2 — fabric/cat.py
CAT(CODE) mínimo — motor de dirimencia que ejecuta código soberano.

Referencia: BIBLIO-SOURCES(CAT-ENGINE).txt §2 CAPA B
No es CAT(OS) ni CAT(SSH) — es la forma mínima verificable:
recibe código Python, lo valida contra gramática LACHO,
lo ejecuta en subprocess controlado, registra resultado.
"""

from __future__ import annotations
import subprocess
import tempfile
import json
import time
import uuid
from pathlib import Path
from typing import Optional

_IMV_DIR = Path(__file__).parent.parent.parent / "IMV"
_IMV_DB  = _IMV_DIR / "data" / "sovereign.db"

# Timeout soberano — tardanza deliberada máxima
_SOVEREIGN_TIMEOUT = 10.0


# ── CAT(CODE) — ejecutor soberano ────────────────────────────────

def cat_code(
    code: str,
    context: Optional[dict] = None,
    tomo_id: Optional[str] = None,
    dry_run: bool = False
) -> dict:
    """
    CAT(CODE) — ejecuta código Python en subprocess soberano.

    Args:
        code: código Python a ejecutar
        context: variables de contexto inyectadas al código
        tomo_id: referencia TOMO para trazabilidad
        dry_run: si True, valida sin ejecutar

    Returns:
        dict con stdout, stderr, returncode, tx_id, status
    """
    tx_id = str(uuid.uuid4())
    ts = time.time()

    # Validación soberana del código
    validation = _validate_code(code)
    if not validation["ok"]:
        return {
            "tx_id": tx_id,
            "operation": "CAT(CODE)",
            "status": "REJECTED",
            "reason": validation["reason"],
            "stdout": "",
            "stderr": "",
            "returncode": -1,
            "tomo_id": tomo_id,
            "duration_ms": 0
        }

    if dry_run:
        return {
            "tx_id": tx_id,
            "operation": "CAT(CODE)",
            "status": "DRY_RUN_OK",
            "stdout": "",
            "stderr": "",
            "returncode": 0,
            "tomo_id": tomo_id,
            "duration_ms": 0
        }

    # Preparar código con contexto inyectado
    full_code = ""
    if context:
        for k, v in context.items():
            full_code += f"{k} = {json.dumps(v)}\n"
    full_code += code

    # Ejecutar en subprocess aislado
    start = time.time()
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.py',
            delete=False, encoding='utf-8'
        ) as f:
            f.write(full_code)
            tmp_path = f.name

        result = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=_SOVEREIGN_TIMEOUT,
            cwd=str(_IMV_DIR)
        )

        Path(tmp_path).unlink(missing_ok=True)

        duration_ms = int((time.time() - start) * 1000)
        status = "OK" if result.returncode == 0 else "ERROR"

    except subprocess.TimeoutExpired:
        Path(tmp_path).unlink(missing_ok=True)
        duration_ms = int(_SOVEREIGN_TIMEOUT * 1000)
        result = type('R', (), {
            'stdout': '', 'stderr': 'TIMEOUT soberano excedido',
            'returncode': -2
        })()
        status = "TIMEOUT"

    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        result = type('R', (), {
            'stdout': '', 'stderr': str(e), 'returncode': -3
        })()
        status = "EXCEPTION"

    # Registrar en ledger
    _log_cat_operation(tx_id, "CAT(CODE)", code[:200], status, tomo_id, ts)

    return {
        "tx_id": tx_id,
        "operation": "CAT(CODE)",
        "status": status,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
        "tomo_id": tomo_id,
        "duration_ms": duration_ms
    }


def _validate_code(code: str) -> dict:
    """
    Validación soberana de código antes de ejecutar.
    Rechaza patrones peligrosos.
    """
    if not code or not code.strip():
        return {"ok": False, "reason": "Código vacío"}

    # Patrones bloqueados soberanamente
    blocked = [
        "import os", "import sys", "import subprocess",
        "__import__", "eval(", "exec(",
        "open(", "os.system", "os.popen",
        "shutil", "socket", "requests",
        "rm -rf", "sudo",
    ]
    code_lower = code.lower()
    for pattern in blocked:
        if pattern.lower() in code_lower:
            return {
                "ok": False,
                "reason": f"Patrón bloqueado: '{pattern}'"
            }

    # Verificar sintaxis Python
    try:
        compile(code, "<sovereign>", "exec")
    except SyntaxError as e:
        return {"ok": False, "reason": f"Sintaxis inválida: {e}"}

    return {"ok": True, "reason": None}


def _log_cat_operation(
    tx_id: str, operation: str, code_preview: str,
    status: str, tomo_id: Optional[str], ts: float
) -> None:
    """Registra operación CAT en ledger soberano."""
    try:
        import sqlite3
        with sqlite3.connect(_IMV_DB) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cat_log (
                    id TEXT PRIMARY KEY,
                    operation TEXT NOT NULL,
                    code_preview TEXT,
                    status TEXT NOT NULL,
                    tomo_id TEXT,
                    timestamp REAL NOT NULL
                )
            """)
            conn.execute("""
                INSERT INTO cat_log
                (id, operation, code_preview, status, tomo_id, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (tx_id, operation, code_preview, status, tomo_id, ts))
            conn.commit()
    except Exception:
        pass


def cat_log(limit: int = 10) -> list[dict]:
    """Retorna el log de operaciones CAT."""
    try:
        import sqlite3
        with sqlite3.connect(_IMV_DB) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM cat_log
                ORDER BY timestamp DESC LIMIT ?
            """, (limit,)).fetchall()
            return [dict(r) for r in rows]
    except Exception:
        return []


# ── Test soberano ─────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("CAT(CODE) — test soberano")
    print("=" * 50)

    # Test básico
    r = cat_code("print('LACHO soberano')", tomo_id="term:A")
    print(f"Status: {r['status']}")
    print(f"Output: {r['stdout'].strip()}")

    # Test con contexto
    r2 = cat_code(
        "print(f'valor={x}')",
        context={"x": 42},
        tomo_id="term:B"
    )
    print(f"Contexto: {r2['stdout'].strip()}")

    # Test bloqueado
    r3 = cat_code("import os; os.system('ls')")
    print(f"Bloqueado: {r3['status']} — {r3['reason']}")

    # Test dry_run
    r4 = cat_code("print('test')", dry_run=True)
    print(f"Dry run: {r4['status']}")

    # Log
    log = cat_log(5)
    print(f"Log: {len(log)} entradas")
    print("=" * 50)
