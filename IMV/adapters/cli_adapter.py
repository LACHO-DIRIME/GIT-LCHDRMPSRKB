"""IMV/adapters/cli_adapter.py — TASK_2.1 [P1][I1]. Only imports from core.ports."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from core.ports import SentencePort
from core.grammar import validate

class CLISentenceAdapter(SentencePort):
    def receive(self, text: str, lang: str = "LACHO") -> dict:
        result = validate(text)
        return {"valid": result.result.value == "VALID",
                "library": getattr(result.library, "value", None),
                "errors": result.errors, "warnings": result.warnings, "source": "CLI"}
