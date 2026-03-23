"""
IMV/core/ports.py — Hexagonal ports. TASK_2.1 [P1][I1]
Closes GAP_4 TIGHT_COUPLING.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


class SentencePort(ABC):
    @abstractmethod
    def receive(self, text: str, lang: str = "LACHO") -> dict: ...

class GlossaryPort(ABC):
    @abstractmethod
    def add_term(self, term: str, library: str, level: int) -> bool: ...

class CrystalPort(ABC):
    @abstractmethod
    def write_crystal(self, transaction: dict) -> str: ...

class ScalarPort(ABC):
    @abstractmethod
    def update_scalar(self, delta: float, reason: str) -> float: ...

class RAGPort(ABC):
    @abstractmethod
    def index_document(self, doc_id: str, content: str, boost: float = 1.0) -> bool: ...


@dataclass
class PortRegistry:
    sentence_port: SentencePort | None = None
    glossary_port: GlossaryPort | None = None
    crystal_port: CrystalPort | None = None
    scalar_port: ScalarPort | None = None
    rag_port: RAGPort | None = None

    def is_complete(self) -> bool:
        return all([self.sentence_port, self.glossary_port,
                    self.crystal_port, self.scalar_port, self.rag_port])

PORTS = PortRegistry()
