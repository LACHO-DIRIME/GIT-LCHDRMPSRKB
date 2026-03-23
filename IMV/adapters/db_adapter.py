"""IMV/adapters/db_adapter.py — CrystalPort + ScalarPort. TASK_2.1"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.ports import CrystalPort, ScalarPort
DB_PATH = Path(__file__).parent.parent / "data" / "sovereign.db"

class SQLiteCrystalAdapter(CrystalPort):
    def write_crystal(self, transaction: dict) -> str:
        from core.ledger import SovereignLedger
        return SovereignLedger(str(DB_PATH)).record(transaction)

class SQLiteScalarAdapter(ScalarPort):
    def update_scalar(self, delta: float, reason: str) -> float:
        from core.ledger import SovereignLedger
        return SovereignLedger(str(DB_PATH)).update_scalar(delta, reason)
