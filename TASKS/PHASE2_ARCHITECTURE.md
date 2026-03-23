# TASKS/PHASE2_ARCHITECTURE.md
# [P1][I1] Systems Architecture — Week 1 Days 4-5, Week 2 Days 1-3
# WHO: Windsurf writes · Claude audits

---

## TASK_2.1 — HEXAGONAL PORTS
### New files: IMV/core/ports.py · IMV/adapters/cli_adapter.py · groq_adapter.py · db_adapter.py
### Priority: [P1][I1] · Gap: GAP_4 TIGHT_MODULE_COUPLING

### IMV/core/ports.py — create this file:

```python
"""
IMV/core/ports.py
Hexagonal architecture port definitions for DIRIME IMV.
Separates domain logic from infrastructure.
[P1][I1] — TASK_2.1
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


# INPUT PORTS — what the domain accepts

class SentencePort(ABC):
    """Receives raw text sentences for grammar validation."""
    @abstractmethod
    def receive(self, text: str, lang: str = "LACHO") -> dict: ...


class GlossaryPort(ABC):
    """Receives new terms for indexing."""
    @abstractmethod
    def add_term(self, term: str, library: str, level: int) -> bool: ...


# OUTPUT PORTS — what the domain emits

class CrystalPort(ABC):
    """Emits crystallized transactions to sovereign.db."""
    @abstractmethod
    def write_crystal(self, transaction: dict) -> str: ...  # returns tx_id


class ScalarPort(ABC):
    """Emits Scalar S updates."""
    @abstractmethod
    def update_scalar(self, delta: float, reason: str) -> float: ...  # returns new S


class RAGPort(ABC):
    """Emits documents to BM25 index."""
    @abstractmethod
    def index_document(self, doc_id: str, content: str, boost: float = 1.0) -> bool: ...


@dataclass
class PortRegistry:
    """Central registry — wire adapters to ports here, not in domain modules."""
    sentence_port: SentencePort | None = None
    glossary_port: GlossaryPort | None = None
    crystal_port: CrystalPort | None = None
    scalar_port: ScalarPort | None = None
    rag_port: RAGPort | None = None

    def is_complete(self) -> bool:
        return all([
            self.sentence_port, self.glossary_port,
            self.crystal_port, self.scalar_port, self.rag_port
        ])


# Singleton registry — imported by main.py at startup
PORTS = PortRegistry()
```

### IMV/adapters/cli_adapter.py — create this file:

```python
"""
IMV/adapters/cli_adapter.py
CLI adapter — implements SentencePort for command-line input.
"""
from __future__ import annotations
from IMV.core.ports import SentencePort
from IMV.core.grammar import validate


class CLISentenceAdapter(SentencePort):
    """Receives sentences from CLI / chat interface."""

    def receive(self, text: str, lang: str = "LACHO") -> dict:
        result = validate(text)
        return {
            "valid": result.valid,
            "library": getattr(result, "library", None),
            "errors": getattr(result, "errors", []),
            "source": "CLI",
        }
```

### IMV/adapters/groq_adapter.py — create this file:

```python
"""
IMV/adapters/groq_adapter.py
Groq adapter — wraps groq/bridge.py with CIRCUIT_BREAKER pattern.
[P2][I2] — TASK_2.4
"""
from __future__ import annotations
import time
from enum import Enum
from IMV.core.ports import SentencePort


class CircuitState(Enum):
    CLOSED   = "CLOSED"     # normal operation
    OPEN     = "OPEN"       # failing — reject requests
    HALF_OPEN= "HALF_OPEN"  # testing recovery


class GroqCircuitBreaker:
    """
    CIRCUIT_BREAKER for Groq API.
    3 failures → OPEN → 30s → HALF_OPEN → test → CLOSED
    """
    FAILURE_THRESHOLD = 3
    RECOVERY_TIMEOUT  = 30  # seconds

    def __init__(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: float = 0.0

    def call(self, fn, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.RECOVERY_TIMEOUT:
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError(f"CIRCUIT_OPEN: Groq unavailable, retry in {self.RECOVERY_TIMEOUT - elapsed:.0f}s")

        try:
            result = fn(*args, **kwargs)
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.FAILURE_THRESHOLD:
                self.state = CircuitState.OPEN
            raise


class GroqSentenceAdapter(SentencePort):
    """Routes natural language → LACHO via Groq, with circuit breaker."""

    def __init__(self):
        self.breaker = GroqCircuitBreaker()

    def receive(self, text: str, lang: str = "LACHO") -> dict:
        try:
            from CAPA_B.groq.bridge import translate_to_lacho
            result = self.breaker.call(translate_to_lacho, text)
            return {"valid": True, "lacho_sentence": result, "source": "GROQ"}
        except RuntimeError as e:
            # Circuit open — activate WHEN_DEFER
            return {"valid": False, "error": str(e), "when_defer": True, "source": "GROQ"}
        except Exception as e:
            return {"valid": False, "error": str(e), "source": "GROQ"}
```

### IMV/adapters/db_adapter.py — create this file:

```python
"""
IMV/adapters/db_adapter.py
Database adapter — implements CrystalPort and ScalarPort for sovereign.db.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
from IMV.core.ports import CrystalPort, ScalarPort

DB_PATH = Path(__file__).parent.parent / "data" / "sovereign.db"


class SQLiteCrystalAdapter(CrystalPort):
    """Writes crystals to sovereign.db via CrystalPort interface."""

    def write_crystal(self, transaction: dict) -> str:
        from IMV.core.ledger import SovereignLedger
        ledger = SovereignLedger(str(DB_PATH))
        return ledger.record(transaction)


class SQLiteScalarAdapter(ScalarPort):
    """Updates Scalar S in sovereign.db via ScalarPort interface."""

    def update_scalar(self, delta: float, reason: str) -> float:
        from IMV.core.ledger import SovereignLedger
        ledger = SovereignLedger(str(DB_PATH))
        return ledger.update_scalar(delta, reason)
```

---

## TASK_2.2 — LIBRARY ISOLATION (BOUNDED_CONTEXT)
### New dir: IMV/libraries/
### Priority: [P1][I2] · Gap: TRUST terms leak into STACKING

### Create IMV/libraries/trust_context.py:

```python
"""IMV/libraries/trust_context.py — TRUST library bounded context."""
LIBRARY_NAME = "TRUST"
SCALAR_MIN   = 0.92
SUBJECTS     = ["FOUNDATION", "[scope]", "[management]", "[term]"]
VERBS        = ["verifica", "establece", "declara", "registra", "certifica"]
HEXAGRAMS    = list(range(1, 9))   # H01-H08
REQUIRES_FOUNDATION = True
```

### Create IMV/libraries/stacking_context.py:

```python
"""IMV/libraries/stacking_context.py — STACKING library bounded context."""
LIBRARY_NAME = "STACKING"
SCALAR_MIN   = 0.85
SUBJECTS     = ["UF[H63]", "UF[H48]", "UF[H52]", "[pillar]", "[crystal]"]
VERBS        = ["cristaliza", "ancla", "apila", "sella", "preserva"]
HEXAGRAMS    = list(range(33, 41))  # H33-H40
REQUIRES_FOUNDATION = False
```

### Create IMV/libraries/crypto_context.py:

```python
"""IMV/libraries/crypto_context.py — CRYPTO library bounded context."""
LIBRARY_NAME = "CRYPTO"
SCALAR_MIN   = 0.88
SUBJECTS     = ["(spark seat)", "(key seat)", "(flow seat)", "(shield seat)"]
VERBS        = ["certifica", "firma", "cifra", "verifica", "sella"]
HEXAGRAMS    = list(range(17, 25))  # H17-H24
REQUIRES_FOUNDATION = True
```

### Create IMV/libraries/gate_context.py:

```python
"""IMV/libraries/gate_context.py — GATE library bounded context."""
LIBRARY_NAME = "GATE"
SCALAR_MIN   = 0.82
SUBJECTS     = ["UF[H06]", "UF[H05]", "[access]", "[barrier]"]
VERBS        = ["bloquea", "filtra", "detiene", "permite", "deniega"]
HEXAGRAMS    = list(range(25, 33))  # H25-H32
REQUIRES_FOUNDATION = False
ABORT_CODES  = ["H05", "H06"]
```

### Create IMV/libraries/samu_context.py:

```python
"""IMV/libraries/samu_context.py — SAMU library bounded context."""
LIBRARY_NAME = "SAMU"
SCALAR_MIN   = 0.88
SUBJECTS     = ["@", "[scalar]", "[dirimencia]", "[coherence]"]
VERBS        = ["dirime", "evalúa", "audita", "resuelve", "delibera"]
HEXAGRAMS    = list(range(9, 17))   # H09-H16
REQUIRES_FOUNDATION = False
DELIBERATE_DELAY_SECONDS = 3
```

---

## TASK_2.3 — EVENT_SOURCING → LEDGER UPGRADE
### File: IMV/core/ledger.py
### Priority: [P2][I2]

Add EVENT_TYPE entries to TransactionType enum in ledger.py:

```python
class TransactionType(Enum):
    # Existing (keep all):
    GRAMMAR_VALIDATION  = "GRAMMAR_VALIDATION"
    SAMU_DIRIMENCE      = "SAMU_DIRIMENCE"
    FOUNDATION_CHECK    = "FOUNDATION_CHECK"
    RED_REGRET          = "RED_REGRET"
    CRYSTAL_RECORD      = "CRYSTAL_RECORD"
    SYSTEM_EVENT        = "SYSTEM_EVENT"
    UNICODE_SWITCH      = "UNICODE_SWITCH"
    TOMO_RECORD         = "TOMO_RECORD"
    # NEW — event sourcing (add these):
    SENTENCE_SUBMITTED  = "SENTENCE_SUBMITTED"
    GRAMMAR_VALIDATED   = "GRAMMAR_VALIDATED"
    SAMU_APPROVED       = "SAMU_APPROVED"
    CRYSTAL_WRITTEN     = "CRYSTAL_WRITTEN"
    SCALAR_UPDATED      = "SCALAR_UPDATED"
    TERM_EXPIRED        = "TERM_EXPIRED"
```

Also add to SovereignLedger class:

```python
def record_event(self, event_type: TransactionType, data: dict) -> str:
    """
    EVENT_SOURCING: record every state transition, not just final state.
    Returns event_id. Each call is append-only — never overwrites.
    """
    tx = Transaction(type=event_type, data=data)
    return self._write_transaction(tx)

def get_history(self, since_timestamp: float = 0.0) -> list[dict]:
    """Returns ordered event log since given timestamp."""
    # ... query sovereign.db for all events ordered by timestamp
```

---

## TASK_2.5 — SAGA_NOTARIA
### File: RUNTIME/RUNNERS/notaria.runner
### Priority: [P2][I2]

Add SAGA compensation comments to notaria.runner workflow:

```
*> SAGA_NOTARIA — compensating transaction flow
*> Each STEP has a named compensating action.
*> If any step fails, execute compensations in reverse order.
*>
*> STEP_1: RECEIVE_DOCUMENT     compensate: REJECT(document)
*> STEP_2: VERIFY_AUTHORITY     compensate: REVOKE(authority_claim)
*> STEP_3: CERTIFY_CRYPTO       compensate: UNSEAL(spark_seat)
*> STEP_4: WRITE_LEDGER         compensate: ROLLBACK_TX(tx_id)
*> STEP_5: EMIT_CRYSTAL_H63     compensate: none (terminal — irreversible)
*>
*> IDEMPOTENCY KEY: document_hash + authority_id + timestamp_day
*> EXACTLY_ONCE: check idempotency_key in sovereign.db before STEP_1
```
