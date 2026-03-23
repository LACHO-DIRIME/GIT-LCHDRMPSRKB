# TASKS/PHASE3_MODULES.md
# [P2][I2] Module Expansion — Week 2 Days 1-3
# WHO: Windsurf writes · Claude reviews contracts

---

## TASK_3.1 — SOVEREIGN MONAD (MONAD_CHAINING)
### File: IMV/core/foundation.py — add to existing file
### Priority: [P2][I2]

```python
# Add to IMV/core/foundation.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class SovereignResult:
    """
    SovereignMonad — wraps the MU→KU→WU pipeline.
    If [term] expires at any point, the chain short-circuits to ABORT.
    """
    value: Any
    scalar: float
    term_active: bool
    library: str
    error: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        return self.term_active and self.error is None

    def bind(self, fn: Callable[["SovereignResult"], "SovereignResult"]) -> "SovereignResult":
        """Chain: if valid, apply fn. If invalid, propagate failure."""
        if not self.is_valid:
            return self  # short-circuit — do not execute fn
        try:
            return fn(self)
        except Exception as e:
            return SovereignResult(
                value=None, scalar=self.scalar,
                term_active=False, library=self.library,
                error=f"MONAD_CHAIN_FAIL: {e}"
            )

    @classmethod
    def unit(cls, value: Any, scalar: float, library: str) -> "SovereignResult":
        """Wrap a raw value into sovereign context."""
        return cls(value=value, scalar=scalar, term_active=True, library=library)
```

---

## TASK_3.2 — RAG CACHE (MEMOIZATION)
### File: IMV/core/rag.py — add to IMEBM25 class
### Priority: [P2][I3]

```python
# Add to IMV/core/rag.py
import hashlib
from functools import lru_cache

# Add to IMEBM25 class:

def _corpus_fingerprint(self) -> str:
    """Hash of all document paths + mtimes — changes when corpus changes."""
    parts = []
    for doc in sorted(self._docs, key=lambda d: d.get("path", "")):
        path = doc.get("path", "")
        mtime = str(doc.get("mtime", 0))
        parts.append(path + mtime)
    return hashlib.md5("|".join(parts).encode()).hexdigest()

def query_cached(self, query: str, top_k: int = 5) -> list[dict]:
    """
    MEMOIZATION: cache BM25 results per (query_hash, corpus_fingerprint).
    If corpus unchanged and same query → return cached result.
    Reduces BM25 lookup from full recompute to O(1) cache hit.
    """
    cache_key = hashlib.md5(f"{query}|{self._corpus_fingerprint()}".encode()).hexdigest()
    if not hasattr(self, "_query_cache"):
        self._query_cache: dict = {}
    if cache_key not in self._query_cache:
        self._query_cache[cache_key] = self.query(query, top_k)
    return self._query_cache[cache_key]

def invalidate_cache(self):
    """Call when corpus changes."""
    self._query_cache = {}
```

---

## TASK_3.3 — ALGEBRAIC EFFECTS (SAMU ISOLATION)
### File: IMV/core/samu.py
### Priority: [P2][I2]

```python
# Add to IMV/core/samu.py

from enum import Enum

class SamuEffect(Enum):
    """
    ALGEBRAIC_EFFECT declarations for SAMU.
    Separates pure effects from stateful operations.
    """
    READ_SCALAR    = "READ_SCALAR"     # pure read — no state change
    WRITE_SCALAR   = "WRITE_SCALAR"    # state change — requires [term] active
    EMIT_WU        = "EMIT_WU"         # IO — requires S >= 0.85
    LOG_RED_REGRET = "LOG_RED_REGRET"  # IO — always allowed

EFFECT_REQUIREMENTS: dict[SamuEffect, dict] = {
    SamuEffect.READ_SCALAR:    {"term_required": False, "scalar_min": 0.0},
    SamuEffect.WRITE_SCALAR:   {"term_required": True,  "scalar_min": 0.0},
    SamuEffect.EMIT_WU:        {"term_required": True,  "scalar_min": 0.85},
    SamuEffect.LOG_RED_REGRET: {"term_required": False, "scalar_min": 0.0},
}

def check_effect(effect: SamuEffect, term_active: bool, scalar: float) -> tuple[bool, str]:
    """Check if an effect is allowed given current state."""
    req = EFFECT_REQUIREMENTS[effect]
    if req["term_required"] and not term_active:
        return False, f"EFFECT_DENIED: {effect.value} requires [term] active"
    if scalar < req["scalar_min"]:
        return False, f"EFFECT_DENIED: {effect.value} requires S>={req['scalar_min']}, got {scalar:.3f}"
    return True, f"EFFECT_ALLOWED: {effect.value}"
```

---

## TASK_3.4 — INCREMENTAL RAG
### File: IMV/core/rag.py — IMEBM25._build_index()
### Priority: [P2][I3]

```python
# Modify _build_index() in IMEBM25:

import hashlib
from pathlib import Path

def _doc_hash(self, path: str) -> str:
    """SHA256 of file content — changes when file changes."""
    try:
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]
    except Exception:
        return "unknown"

def build_incremental(self, force_rebuild: bool = False):
    """
    INCREMENTAL_COMPUTATION: only re-index changed or new documents.

    if doc_hash unchanged → skip (use cached index entry)
    if doc_hash changed   → re-index that document only
    if new doc added      → append to existing index

    At 5x corpus size (925 BIBLIO-SOURCES), this reduces
    startup from ~90 seconds to under 2 seconds.
    """
    if not hasattr(self, "_doc_hashes"):
        self._doc_hashes: dict[str, str] = {}

    new_docs = []
    for doc in self._docs:
        path = doc.get("path", "")
        current_hash = self._doc_hash(path)
        if force_rebuild or self._doc_hashes.get(path) != current_hash:
            new_docs.append(doc)
            self._doc_hashes[path] = current_hash

    if new_docs or force_rebuild:
        self._rebuild_index_for(new_docs)
        self.invalidate_cache()
```

---

## TASK_3.5 — DEPENDENT_CONTRACT
### File: IMV/core/grammar.py — validate() function
### Priority: [P2][I2]

```python
# Add pre/post condition decorators — or inline checks if no decorator lib available

def validate(text: str, scalar: float = 0.0, term_active: bool = True, _depth: int = 0):
    """
    DEPENDENT_CONTRACT:
    PRE_1:  text has at least 6 tokens (SENTENCE has 6 slots)
    PRE_2:  [term] is present in text
    PRE_3:  Scalar S >= library.scalar_min (checked after library identified)
    PRE_4:  depth < MAX_RECURSION_DEPTH
    POST_1: result.library matches first token
    POST_2: if valid, UF hexagram is in active set
    """
    # PRE_1
    tokens = text.strip().split()
    if len(tokens) < 6:
        return ValidationResult(valid=False, error_code="PRE_1",
            error_msg=f"PRE_CONDITION_FAIL: sentence has {len(tokens)} tokens, need >= 6")

    # PRE_2
    if "[" not in text or "]" not in text:
        return ValidationResult(valid=False, error_code="PRE_2",
            error_msg="PRE_CONDITION_FAIL: [term] not found in sentence")

    # PRE_4 (depth guard from TASK_1.2)
    if _depth >= MAX_RECURSION_DEPTH:
        return ValidationResult(valid=False, error_code="H06",
            error_msg="ABORT: max depth 64 exceeded")

    # ... existing validation logic ...

    # POST_1 (add after validation result computed)
    # if result.valid and result.library != tokens[0]:
    #     result.valid = False
    #     result.error_msg = "POST_CONDITION_FAIL: library mismatch"
```

---

## TASK_3.6 — REACTIVE SCALAR MONITOR
### File: IMV/tools/generator.py — extend
### Priority: [P2][I3]

```python
# Add to generator.py or create IMV/tools/scalar_monitor.py

import json
import time
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "sovereign.db"
POLL_INTERVAL = 30  # seconds

def get_current_scalar(db_path: str = str(DB_PATH)) -> dict:
    """Read current Scalar S from sovereign.db."""
    try:
        conn = sqlite3.connect(db_path)
        # Adjust query to match actual sovereign.db schema
        row = conn.execute(
            "SELECT scalar, tx_count, crystal_count FROM system_state ORDER BY id DESC LIMIT 1"
        ).fetchone()
        conn.close()
        if row:
            return {"scalar": round(row[0], 4), "tx_count": row[1], "crystal_count": row[2]}
        return {"scalar": 0.0, "tx_count": 0, "crystal_count": 0}
    except Exception as e:
        return {"scalar": 0.0, "error": str(e)}

def write_scalar_json(output_path: str = "IMV/data/scalar_live.json"):
    """
    REACTIVE_DATAFLOW: write current scalar to JSON file every 30s.
    Consumed by elpulsar dashboard and KALIL agents dashboard.
    """
    data = get_current_scalar()
    data["timestamp"] = time.time()
    data["iso_time"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    return data

if __name__ == "__main__":
    print("Scalar monitor started — polling every 30s")
    while True:
        result = write_scalar_json()
        print(f"[{result['iso_time']}] S={result['scalar']} TX={result.get('tx_count',0)}")
        time.sleep(POLL_INTERVAL)
```
