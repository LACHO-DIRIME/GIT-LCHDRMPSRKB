"""IMV/adapters/groq_adapter.py — CIRCUIT_BREAKER. TASK_2.4 [P2][I2]."""
from __future__ import annotations
import sys, time
from pathlib import Path
from enum import Enum
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.ports import SentencePort

class CircuitState(Enum):
    CLOSED="CLOSED"; OPEN="OPEN"; HALF_OPEN="HALF_OPEN"

class GroqCircuitBreaker:
    FAILURE_THRESHOLD=3; RECOVERY_TIMEOUT=30
    def __init__(self):
        self.state=CircuitState.CLOSED; self.failure_count=0; self.last_failure_time=0.0
    def call(self, fn, *args, **kwargs):
        if self.state==CircuitState.OPEN:
            elapsed=time.time()-self.last_failure_time
            if elapsed>=self.RECOVERY_TIMEOUT: self.state=CircuitState.HALF_OPEN
            else: raise RuntimeError(f"CIRCUIT_OPEN: retry in {self.RECOVERY_TIMEOUT-elapsed:.0f}s")
        try:
            result=fn(*args,**kwargs)
            if self.state==CircuitState.HALF_OPEN: self.state=CircuitState.CLOSED; self.failure_count=0
            return result
        except Exception:
            self.failure_count+=1; self.last_failure_time=time.time()
            if self.failure_count>=self.FAILURE_THRESHOLD: self.state=CircuitState.OPEN
            raise

class GroqSentenceAdapter(SentencePort):
    def __init__(self): self.breaker=GroqCircuitBreaker()
    def receive(self, text: str, lang: str="LACHO") -> dict:
        try:
            from CAPA_B.groq.bridge import translate_to_lacho
            r=self.breaker.call(translate_to_lacho, text)
            return {"valid": True, "lacho_sentence": r, "source": "GROQ"}
        except RuntimeError as e:
            return {"valid": False, "error": str(e), "when_defer": True, "source": "GROQ"}
        except Exception as e:
            return {"valid": False, "error": str(e), "source": "GROQ"}
