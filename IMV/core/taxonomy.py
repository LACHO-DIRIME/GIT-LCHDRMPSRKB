"""
DIRIME IMV — taxonomy.py
Taxonomía soberana LACHO para clasificación de confianza notarial.

Referencia canónica:
  BIBLIO-SOURCES(TAXONOMY_LACHO).txt
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class TaxonomyLevel:
    """Nivel de confianza en taxonomía soberana."""
    level: int
    name: str
    scalar_min: float
    class_name: str
    libraries: list[str]
    description: str


class TaxonomyLACHO:
    """Taxonomía soberana LACHO para clasificación notarial."""
    
    # Niveles de confianza notarial
    N0 = TaxonomyLevel(
        level=0,
        name="TRUST",
        scalar_min=0.92,
        class_name="nucleo",
        libraries=["TRUST"],
        description="Requiere acto certifica - nivel más alto de confianza"
    )
    
    N1 = TaxonomyLevel(
        level=1,
        name="SAMU+CRYPTO",
        scalar_min=0.88,
        class_name="auditor_notarial",
        libraries=["SAMU", "CRYPTO"],
        description="Mínimo para NOTARIA - auditoría y certificación"
    )
    
    N2 = TaxonomyLevel(
        level=2,
        name="GATE+STACKING",
        scalar_min=0.85,
        class_name="protocolo",
        libraries=["GATE", "STACKING"],
        description="Protocolo de validación y almacenamiento"
    )
    
    N3 = TaxonomyLevel(
        level=3,
        name="WORK+SOCIAL+ACTIVITY",
        scalar_min=0.82,
        class_name="ejecucion",
        libraries=["WORK", "SOCIAL", "ACTIVITY"],
        description="Ejecución y operaciones sociales"
    )
    
    N4 = TaxonomyLevel(
        level=4,
        name="METHOD",
        scalar_min=0.80,
        class_name="calculador",
        libraries=["METHOD"],
        description="Cálculos y procesamiento de datos"
    )
    
    # Todos los niveles en orden
    LEVELS = [N0, N1, N2, N3, N4]
    
    @classmethod
    def classify(cls, scalar: float) -> TaxonomyLevel:
        """Clasifica un valor scalar en el nivel de taxonomía correspondiente."""
        for level in cls.LEVELS:
            if scalar >= level.scalar_min:
                return level
        # Si no alcanza ningún nivel, retorna el más bajo con advertencia
        return cls.N4
    
    @classmethod
    def is_notaria_valid(cls, scalar: float) -> bool:
        """Verifica si el scalar cumple mínimo para NOTARIA (N1+)."""
        return scalar >= cls.N1.scalar_min  # >= 0.88
    
    @classmethod
    def is_certifica_valid(cls, scalar: float) -> bool:
        """Verifica si el scalar cumple mínimo para acto_certifica (N0)."""
        return scalar >= cls.N0.scalar_min  # >= 0.92
    
    @classmethod
    def get_level_by_name(cls, name: str) -> Optional[TaxonomyLevel]:
        """Obtiene nivel de taxonomía por nombre."""
        for level in cls.LEVELS:
            if level.name == name:
                return level
        return None
    
    @classmethod
    def get_level_by_library(cls, library: str) -> Optional[TaxonomyLevel]:
        """Obtiene nivel de taxonomía por biblioteca."""
        for level in cls.LEVELS:
            if library in level.libraries:
                return level
        return None
    
    @classmethod
    def validate_notaria_operation(cls, scalar: float, operation: str) -> tuple[bool, str]:
        """Valida si una operación notarial es permitida con el scalar dado."""
        if operation == "certifica":
            valid = cls.is_certifica_valid(scalar)
            reason = "acto_certifica requiere N0 (scalar >= 0.92)" if not valid else "Certificación permitida"
        elif operation in ["sella", "inmutabiliza"]:
            valid = cls.is_notaria_valid(scalar)
            reason = "NOTARIA requiere N1+ (scalar >= 0.88)" if not valid else "Operación notarial permitida"
        else:
            # Para otras operaciones, se requiere mínimo N2
            valid = scalar >= cls.N2.scalar_min
            reason = f"Operación '{operation}' requiere N2+ (scalar >= 0.85)" if not valid else "Operación permitida"
        
        return valid, reason
    
    @classmethod
    def get_taxonomy_summary(cls) -> dict:
        """Obtiene resumen completo de la taxonomía."""
        return {
            "levels": [
                {
                    "level": level.level,
                    "name": level.name,
                    "scalar_min": level.scalar_min,
                    "class": level.class_name,
                    "libraries": level.libraries,
                    "description": level.description
                }
                for level in cls.LEVELS
            ],
            "notaria_min": cls.N1.scalar_min,
            "certifica_min": cls.N0.scalar_min,
            "protocol_min": cls.N2.scalar_min,
            "total_levels": len(cls.LEVELS)
        }


# Funciones de conveniencia para uso en grammar.py
def classify_scalar(scalar: float) -> TaxonomyLevel:
    """Función de conveniencia para clasificar scalar."""
    return TaxonomyLACHO.classify(scalar)


def is_notaria_allowed(scalar: float) -> bool:
    """Función de conveniencia para validar operaciones notariales."""
    return TaxonomyLACHO.is_notaria_valid(scalar)


def is_certifica_allowed(scalar: float) -> bool:
    """Función de conveniencia para validar certificación."""
    return TaxonomyLACHO.is_certifica_valid(scalar)
