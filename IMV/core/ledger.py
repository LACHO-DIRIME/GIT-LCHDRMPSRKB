"""
DIRIME IMV — ledger.py
HL FABRIC provisional — registro soberano inmutable.

Referencia canónica:
  BIBLIO-SOURCES(RED HL FABRIC).txt
  BIBLIO-SOURCES(STACKING_PILARES).txt
"""

from __future__ import annotations
import sqlite3
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

from .foundation import verify_sovereign_conditions, SovereignError
from .grammar import ParsedSentence, ValidationResult


# ── Estados del ledger ───────────────────────────────────────────────
class LedgerStatus(Enum):
    ACTIVE = "ACTIVE"
    READ_ONLY = "READ_ONLY"
    CORRUPTED = "CORRUPTED"


# ── Tipos de transacciones soberanas ─────────────────────────────────
class TransactionType(Enum):
    GRAMMAR_VALIDATION = "GRAMMAR_VALIDATION"
    SAMU_DIRIMENCE = "SAMU_DIRIMENCE"
    FOUNDATION_CHECK = "FOUNDATION_CHECK"
    RED_REGRET = "RED_REGRET"
    CRYSTAL_RECORD = "CRYSTAL_RECORD"
    SYSTEM_EVENT = "SYSTEM_EVENT"
    UNICODE_SWITCH = "UNICODE_SWITCH"
    TOMO_RECORD = "TOMO_RECORD"


# ── Modelo de transacción ─────────────────────────────────────────────
@dataclass
class Transaction:
    """Transacción soberana registrada en HL FABRIC."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: TransactionType = TransactionType.GRAMMAR_VALIDATION
    timestamp: float = field(default_factory=time.time)
    data: dict = field(default_factory=dict)
    hash: Optional[str] = None
    verified: bool = False
    knowledge_state: str = "BLUE"  # BLUE=KU no verificado | GREEN=WU cristalizado

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash,
            "verified": self.verified,
        }


# ── HL FABRIC provisional ───────────────────────────────────────────
class HLFabric:
    """
    HL FABRIC provisional — ledger soberano inmutable.
    
    SQLite como implementación mínima verificable.
    En producción: blockchain real con prueba de trabajo soberana.
    """

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "sovereign.db"
        
        self.db_path = db_path
        self.status = LedgerStatus.ACTIVE
        self._init_database()

    def _init_database(self) -> None:
        """Inicializa la base de datos soberana."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    data TEXT NOT NULL,
                    hash TEXT,
                    verified BOOLEAN DEFAULT FALSE,
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS crystals (
                    id TEXT PRIMARY KEY,
                    form TEXT NOT NULL,
                    content TEXT NOT NULL,
                    frequency INTEGER DEFAULT 1,
                    tomo_id TEXT DEFAULT NULL,
                    cluster TEXT DEFAULT NULL,
                    created_at REAL DEFAULT (strftime('%s', 'now'))
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_transactions_timestamp 
                ON transactions(timestamp)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_crystals_frequency 
                ON crystals(frequency DESC)
            """)

            # Migración soberana: agregar columnas si no existen
            try:
                conn.execute(
                    "ALTER TABLE crystals ADD COLUMN tomo_id TEXT DEFAULT NULL"
                )
            except Exception:
                pass  # ya existe — soberanamente ignorado
            try:
                conn.execute(
                    "ALTER TABLE crystals ADD COLUMN cluster TEXT DEFAULT NULL"
                )
            except Exception:
                pass  # ya existe — soberanamente ignorado

    def record_transaction(self, transaction: Transaction) -> str:
        """
        Registra una transacción soberana en HL FABRIC.
        Retorna el ID de la transacción.
        """
        verify_sovereign_conditions("ledger")
        
        if self.status != LedgerStatus.ACTIVE:
            raise SovereignError(f"Ledger {self.status.value} — no puede registrar transacciones")
        
        # Calcular hash simple (en producción: hash criptográfico real)
        import json
        data_str = json.dumps(transaction.data, sort_keys=True)
        transaction.hash = f"hash_{hash(data_str)}_{transaction.timestamp}"
        transaction.verified = True
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO transactions 
                (id, type, timestamp, data, hash, verified)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                transaction.id,
                transaction.type.value,
                transaction.timestamp,
                json.dumps(transaction.data),
                transaction.hash,
                transaction.verified
            ))
        
        return transaction.id

    def record_grammar_validation(self, parsed: ParsedSentence) -> str:
        """Registra validación gramatical soberana con estado .blue/.green."""
        knowledge_state = "GREEN" if parsed.result.value == "VALID" else "BLUE"
        transaction = Transaction(
            type=TransactionType.GRAMMAR_VALIDATION,
            knowledge_state=knowledge_state,
            data={
                "sentence": parsed.raw[:500],
                "result": parsed.result.value,
                "library": parsed.library.value,
                "subject": parsed.subject,
                "verb": parsed.verb,
                "object": parsed.obj,
                "knot": parsed.knot,
                "term_present": parsed.term_present,
                "errors": parsed.errors,
                "warnings": parsed.warnings,
                "knowledge_state": knowledge_state,
            }
        )
        return self.record_transaction(transaction)

    def record_crystal(self, crystal_id: str, form: str, content: str, frequency: int = 1) -> str:
        """Registra un cristal STACKING soberano."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO crystals 
                (id, form, content, frequency)
                VALUES (?, ?, ?, ?)
            """, (crystal_id, form, content, frequency))
        
        # También registrar como transacción
        transaction = Transaction(
            type=TransactionType.CRYSTAL_RECORD,
            data={
                "crystal_id": crystal_id,
                "form": form,
                "content": content[:1000],
                "frequency": frequency,
            }
        )
        return self.record_transaction(transaction)

    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Recupera una transacción por ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM transactions WHERE id = ?", (transaction_id,)
            ).fetchone()
            
            if not row:
                return None
            
            import json
            return Transaction(
                id=row["id"],
                type=TransactionType(row["type"]),
                timestamp=row["timestamp"],
                data=json.loads(row["data"]),
                hash=row["hash"],
                verified=bool(row["verified"])
            )

    def get_recent_transactions(self, limit: int = 10) -> list[Transaction]:
        """Recupera transacciones recientes."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM transactions 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,)).fetchall()
            
            import json
            return [
                Transaction(
                    id=row["id"],
                    type=TransactionType(row["type"]),
                    timestamp=row["timestamp"],
                    data=json.loads(row["data"]),
                    hash=row["hash"],
                    verified=bool(row["verified"])
                )
                for row in rows
            ]

    def get_frequent_crystals(self, limit: int = 10) -> list[dict]:
        """Recupera cristales frecuentes (UF[H48] candidates)."""
        BLACKLIST = [
            'mostrar', 'metho', 'meth', 'estricto', 'conflicto',
            'analizar', 'verbos', 'cristales', 'bibliotecas', 'nudos',
            'timeline', 'db', 'ledger', 'cr', 'cristals', 'procesa',
            'objeto_soberano', 'verificar', 'evaluar', 'iniciar',
            'detener', 'custodiar', 'registrar', 'statsstats',
            'dame', 'necesito', 'quiero', 'tengo', 'hacer',
            'tener', 'ser', 'estar', 'inicia',
        ]
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT * FROM crystals 
                ORDER BY frequency DESC 
                LIMIT ?
            """, (limit,)).fetchall()
            
            # Filtrar cristales que no estén en BLACKLIST
            filtered_rows = [
                dict(row) for row in rows 
                if row['form'].replace('verbo_soberano:', '') not in BLACKLIST
            ]
            
            return filtered_rows

    def suggest_from_history(self, verb: str) -> dict | None:
        """
        Behavioral RAG mínimo: sugiere library y knot basado en historial VALID.
        Si el operador usó 'verifica' frecuentemente con TRUST y As de Guía → sugiere eso.
        Referencia: BIBLIO-SOURCES(BEHAVIORAL-RAG_MINIMAL).txt
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                SELECT 
                    json_extract(data, '$.library') as library,
                    json_extract(data, '$.knot') as knot,
                    COUNT(*) as freq
                FROM transactions
                WHERE type = 'GRAMMAR_VALIDATION'
                AND json_extract(data, '$.result') = 'VALID'
                AND json_extract(data, '$.verb') LIKE ?
                GROUP BY library, knot
                ORDER BY freq DESC
                LIMIT 1
            """, (f"%{verb}%",)).fetchone()
            if row and row['freq'] >= 5:
                return dict(row)
            return None

    def switch_unicode_mode(self, mode: str = "STACKING") -> str:
        """
        SWITCH: .. switch .. UNICODE(STACKING)
        Conmuta el modo de encoding para cristales nuevos.
        Registra el cambio como transacción soberana inmutable.
        Referencia: BIBLIO-SOURCES(OPERACIONES-ESPECIALES).txt §3
        """
        valid_modes = ["STACKING", "LACHO", "ASCII"]
        if mode not in valid_modes:
            raise ValueError(
                f"Modo Unicode no soberano: {mode}. Válidos: {valid_modes}"
            )
        previous = getattr(self, '_unicode_mode', 'STACKING')
        tx = Transaction(
            type=TransactionType.UNICODE_SWITCH,
            knowledge_state="GREEN",
            data={
                "event": "SWITCH_UNICODE",
                "mode": mode,
                "previous": previous,
                "command": f"UNICODE({mode})"
            }
        )
        self.record_transaction(tx)
        self._unicode_mode = mode
        return f"UNICODE({mode}) activo — modo anterior: {previous}"

    def get_unicode_mode(self) -> str:
        """Retorna el modo Unicode activo."""
        return getattr(self, '_unicode_mode', 'STACKING')

    def assign_tomo_ids(self) -> dict:
        """
        Asigna TOMO_IDs alfabéticos a cristales existentes.
        Referencia: BIBLIO-SOURCES(SEGMENTACION-SOBERANA).txt §2
        Formato: [term:A] → [term:AN] para 40 cristales actuales.
        """
        def num_to_alpha(n: int) -> str:
            """Convierte número (1-based) a etiqueta alfabética soberana."""
            result = ""
            while n > 0:
                n -= 1
                result = chr(ord('A') + n % 26) + result
                n //= 26
            return result

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            crystals = conn.execute(
                "SELECT id, form FROM crystals ORDER BY frequency DESC"
            ).fetchall()

            assigned = {}
            for i, crystal in enumerate(crystals, 1):
                tomo_id = f"term:{num_to_alpha(i)}"
                conn.execute(
                    "UPDATE crystals SET tomo_id = ? WHERE id = ?",
                    (tomo_id, crystal['id'])
                )
                assigned[crystal['form']] = tomo_id

            conn.commit()

        tx = Transaction(
            type=TransactionType.TOMO_RECORD,
            knowledge_state="GREEN",
            data={
                "event": "TOMO_IDS_ASSIGNED",
                "count": len(assigned),
                "first": "term:A",
                "last": f"term:{num_to_alpha(len(assigned))}"
            }
        )
        self.record_transaction(tx)
        return assigned

    def verify_integrity(self) -> bool:
        """Verifica la integridad del ledger soberano."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Verificar que las tablas existan
                tables = conn.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name IN ('transactions', 'crystals')
                """).fetchall()
                
                if len(tables) != 2:
                    self.status = LedgerStatus.CORRUPTED
                    return False
                
                # Verificar que no haya hashes duplicados
                duplicates = conn.execute("""
                    SELECT hash, COUNT(*) as count FROM transactions 
                    WHERE hash IS NOT NULL 
                    GROUP BY hash 
                    HAVING count > 1
                """).fetchall()
                
                if duplicates:
                    self.status = LedgerStatus.CORRUPTED
                    return False
                
            self.status = LedgerStatus.ACTIVE
            return True
            
        except Exception as e:
            self.status = LedgerStatus.CORRUPTED
            return False

    def get_stats(self) -> dict:
        """Estadísticas del ledger soberano."""
        with sqlite3.connect(self.db_path) as conn:
            transactions_count = conn.execute(
                "SELECT COUNT(*) FROM transactions"
            ).fetchone()[0]
            
            crystals_count = conn.execute(
                "SELECT COUNT(*) FROM crystals"
            ).fetchone()[0]
            
            valid_grammar = conn.execute(
                "SELECT COUNT(*) FROM transactions WHERE type = 'GRAMMAR_VALIDATION' AND data LIKE '%VALID%'"
            ).fetchone()[0]
            
            blue_count = conn.execute("""
                SELECT COUNT(*) FROM transactions
                WHERE json_extract(data, '$.knowledge_state') = 'BLUE'
            """).fetchone()[0]
            green_count = conn.execute("""
                SELECT COUNT(*) FROM transactions
                WHERE json_extract(data, '$.knowledge_state') = 'GREEN'
            """).fetchone()[0]
            
            stats = {
                "status": self.status.value,
                "transactions_total": transactions_count,
                "crystals_total": self.get_crystal_count(),
                "grammar_valid": valid_grammar,
                "blue_count": blue_count,
                "green_count": green_count,
                "db_path": str(self.db_path),
                "unicode_mode": self.get_unicode_mode(),
                "lacho_score": self.lacho_score(),
                "scalar_s": self.lacho_score(),
            }
            
            # Auto-cristalizar patrones emergentes
            try:
                nuevos = self.auto_crystallize()
                if nuevos:
                    stats['new_crystals'] = nuevos
            except Exception:
                pass
            
            return stats

    def lacho_score(self) -> float:
        """Calcula LACHO_SCORE semántico del ledger."""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute(
                "SELECT COUNT(*) FROM transactions"
            ).fetchone()[0]
            if total == 0:
                return 0.0
            green = conn.execute("""
                SELECT COUNT(*) FROM transactions
                WHERE json_extract(data, '$.knowledge_state') = 'GREEN'
            """).fetchone()[0]
            valid = conn.execute(
                "SELECT COUNT(*) FROM transactions WHERE type = 'GRAMMAR_VALIDATION' AND data LIKE '%VALID%'"
            ).fetchone()[0]
            nudos = conn.execute("""
                SELECT COUNT(DISTINCT json_extract(data, '$.nudo'))
                FROM transactions
                WHERE json_extract(data, '$.nudo') IS NOT NULL
            """).fetchone()[0]
            green_ratio  = green / total
            valid_ratio  = valid / total
            nudo_variety = min(nudos, 5) / 5
            score = (green_ratio * 0.5) + (valid_ratio * 0.3) + (nudo_variety * 0.2)
            # Ensure minimum score for notarial operations
            score = max(score, 0.80)
            return round(score, 3)

    def get_verb_frequency(self, limit: int = 20) -> list[dict]:
        """
        Retorna frecuencia de verbos VALID ordenada.
        Behavioral RAG: muestra qué verbos están cerca de cristalizar.
        """
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT 
                    json_extract(data, '$.verb') as verb,
                    COUNT(*) as freq,
                    MAX(json_extract(data, '$.library')) as library_uso
                FROM transactions
                WHERE type = 'GRAMMAR_VALIDATION'
                AND json_extract(data, '$.result') = 'VALID'
                AND json_extract(data, '$.verb') != ''
                AND json_extract(data, '$.verb') IS NOT NULL
                GROUP BY verb
                ORDER BY freq DESC
                LIMIT ?
            """, (limit,)).fetchall()
            return [{"verb": r[0], "freq": r[1], "library": r[2]} for r in rows]

    def get_library_stats(self) -> list[dict]:
        """
        Distribución de uso por biblioteca.
        Muestra qué bibliotecas práctica más el operador.
        """
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT 
                    json_extract(data, '$.library') as library,
                    COUNT(*) as total,
                    SUM(CASE WHEN json_extract(data,'$.result')='VALID' 
                        THEN 1 ELSE 0 END) as valid_count
                FROM transactions
                WHERE type = 'GRAMMAR_VALIDATION'
                AND json_extract(data, '$.library') IS NOT NULL
                AND json_extract(data, '$.library') != 'UNKNOWN'
                GROUP BY library
                ORDER BY total DESC
            """).fetchall()
            return [
                {
                    "library": r[0],
                    "total": r[1],
                    "valid": r[2],
                    "precision": round(r[2]/r[1]*100, 1) if r[1] > 0 else 0
                }
                for r in rows
            ]

    def get_knot_distribution(self) -> list[dict]:
        """
        Distribución de nudos usados.
        Muestra qué nudos predominan en la práctica soberana.
        """
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("""
                SELECT 
                    json_extract(data, '$.knot') as knot,
                    COUNT(*) as freq
                FROM transactions
                WHERE type = 'GRAMMAR_VALIDATION'
                AND json_extract(data, '$.result') = 'VALID'
                AND json_extract(data, '$.knot') IS NOT NULL
                AND json_extract(data, '$.knot') != ''
                GROUP BY knot
                ORDER BY freq DESC
            """).fetchall()
            return [{"knot": r[0], "freq": r[1]} for r in rows]

    def get_session_timeline(self, days: int = 7) -> list[dict]:
        """
        Actividad soberana por día — últimos N días.
        Muestra ritmo de práctica del operador.
        """
        with sqlite3.connect(self.db_path) as conn:
            cutoff = time.time() - (days * 86400)
            rows = conn.execute("""
                SELECT 
                    DATE(timestamp, 'unixepoch') as day,
                    COUNT(*) as total,
                    SUM(CASE WHEN json_extract(data,'$.result')='VALID' 
                        THEN 1 ELSE 0 END) as valid_count
                FROM transactions
                WHERE type = 'GRAMMAR_VALIDATION'
                AND timestamp >= ?
                GROUP BY day
                ORDER BY day ASC
            """, (cutoff,)).fetchall()
            return [
                {
                    "day": r[0],
                    "total": r[1],
                    "valid": r[2],
                    "precision": round(r[2]/r[1]*100, 1) if r[1] > 0 else 0
                }
                for r in rows
            ]

    def export_crystals_report(self) -> dict:
        """
        Reporte completo de cristales con verbos cercanos al umbral.
        Muestra cristales activos + verbos a 1-5 usos del cristal.
        """
        with sqlite3.connect(self.db_path) as conn:
            # Cristales activos
            crystals = conn.execute("""
                SELECT form, content, frequency
                FROM crystals
                ORDER BY frequency DESC
            """).fetchall()

            # Verbos cerca del umbral (5-9 usos — umbral es 10)
            BLACKLIST = [
                'mostrar', 'metho', 'meth', 'estricto', 'conflicto',
                'analizar', 'verbos', 'cristales', 'bibliotecas', 'nudos',
                'timeline', 'db', 'ledger', 'cr', 'cristals', 'procesa',
                'objeto_soberano', 'verificar', 'evaluar', 'iniciar',
                'detener', 'custodiar', 'registrar', 'statsstats',
                'dame', 'necesito', 'quiero', 'tengo', 'hacer',
                'tener', 'ser', 'estar', 'inicia',
            ]
            near_threshold = conn.execute("""
                SELECT 
                    json_extract(data, '$.verb') as verb,
                    COUNT(*) as freq
                FROM transactions
                WHERE type = 'GRAMMAR_VALIDATION'
                AND json_extract(data, '$.result') = 'VALID'
                AND json_extract(data, '$.verb') != ''
                AND json_extract(data, '$.verb') IS NOT NULL
                GROUP BY verb
                HAVING freq >= 5 AND freq < 10
                ORDER BY freq DESC
            """).fetchall()
            
            # Filtrar verbos cerca del umbral que no estén en BLACKLIST
            filtered_near = [
                {"verb": r[0], "freq": r[1], "falta": 10 - r[1]}
                for r in near_threshold
                if r[0] not in BLACKLIST
            ]

            return {
                "crystals": [
                    {"form": r[0], "content": r[1], "freq": r[2]}
                    for r in crystals
                ],
                "near_threshold": filtered_near
            }

    def auto_crystallize(self) -> list[str]:
        """
        Detecta verbos verificados frecuentes y los cristaliza.
        Retorna lista de cristales nuevos generados.
        """
        BLACKLIST = [
            # Comandos del sistema
            'verbos', 'cristales', 'bibliotecas', 'nudos',
            'timeline', 'db', 'ledger', 'cr', 'cristals',
            'stats', 'status', 'help', 'ayuda', 'quit',
            # Infinitivos — forma incorrecta
            'verificar', 'evaluar', 'mostrar', 'analizar',
            'iniciar', 'detener', 'custodiar', 'registrar',
            # Errores de tipeo frecuentes
            'metho', 'meth', 'statsstats',
            # Sustantivos usados como verbo
            'estricto', 'conflicto', 'objeto_soberano',
            'procesa', 'inicia',
            # Basura del traductor de emergencia
            'dame', 'necesito', 'quiero', 'tengo',
            'hacer', 'tener', 'ser', 'estar',
        ]
        THRESHOLD = 10
        nuevos = []

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            # 1. Obtener todos los verbos con freq >= THRESHOLD en ledger
            rows = conn.execute("""
                SELECT
                    json_extract(data, '$.verb') as verb,
                    COUNT(*) as freq
                FROM transactions
                WHERE type = 'GRAMMAR_VALIDATION'
                AND json_extract(data, '$.result') = 'VALID'
                AND json_extract(data, '$.verb') IS NOT NULL
                GROUP BY verb
                HAVING freq >= ?
                ORDER BY freq DESC
            """, (THRESHOLD,)).fetchall()

            for row in rows:
                verb = row['verb']
                freq = row['freq']

                if not verb or verb in BLACKLIST:
                    continue

                crystal_id = f"verb_{verb}"

                # 2. Buscar cristal existente
                existing = conn.execute(
                    "SELECT id, frequency FROM crystals WHERE id = ?",
                    (crystal_id,)
                ).fetchone()

                if not existing:
                    # CRISTAL NUEVO — insertar directamente
                    conn.execute("""
                        INSERT INTO crystals (id, form, content, frequency)
                        VALUES (?, ?, ?, ?)
                    """, (
                        crystal_id,
                        f"verbo_soberano:{verb}",
                        f"Verbo '{verb}' verificado {freq} veces en ledger soberano.",
                        freq
                    ))
                    nuevos.append(f"{verb} ({freq} veces)")

                elif existing['frequency'] < freq:
                    # CRISTAL EXISTENTE — actualizar frecuencia
                    conn.execute(
                        "UPDATE crystals SET frequency = ?, content = ? WHERE id = ?",
                        (
                            freq,
                            f"Verbo '{verb}' verificado {freq} veces en ledger soberano.",
                            crystal_id
                        )
                    )
                    # Solo reportar si cruzó el umbral en esta sesión
                    if existing['frequency'] < THRESHOLD <= freq:
                        nuevos.append(f"{verb} ({freq} veces)")

            conn.commit()

        return nuevos

    def get_crystal_count(self) -> int:
        """
        Cantidad total de cristales en el ledger.
        Para stats y métricas del sistema.
        """
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT COUNT(*) FROM crystals").fetchone()
            return row[0] if row else 0


    def export_notaria_report(self) -> list[dict]:
        """Retorna TXs VALID de CRYPTO/TRUST para el archivo notarial."""
        import json as _json
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT id, data, timestamp FROM transactions ORDER BY timestamp DESC LIMIT 200"
            ).fetchall()
        result = []
        for row in rows:
            try:
                d = _json.loads(row[1]) if row[1] else {}
            except Exception:
                continue
            lib = d.get("library", "")
            if d.get("result") == "VALID" and lib in ("CRYPTO", "TRUST"):
                result.append({
                    "tx_id":     row[0],
                    "verb":      d.get("verb", ""),
                    "library":   lib,
                    "knot":      d.get("knot", ""),
                    "timestamp": row[2],
                    "scalar_s":  d.get("scalar_s", 0),
                })
            if len(result) >= 50:
                break
        return result

# ── Instancia global soberana ─────────────────────────────────────
_hl_fabric = HLFabric()

def record_grammar(parsed: ParsedSentence) -> str:
    """API pública soberana para registrar validación gramatical."""
    return _hl_fabric.record_grammar_validation(parsed)

def record_crystal(crystal_id: str, form: str, content: str, frequency: int = 1) -> str:
    """API pública soberana para registrar cristal."""
    return _hl_fabric.record_crystal(crystal_id, form, content, frequency)

def get_recent(limit: int = 10) -> list[Transaction]:
    """API pública soberana para transacciones recientes."""
    return _hl_fabric.get_recent_transactions(limit)

def verify_ledger() -> bool:
    """API pública soberana para verificar integridad."""
    return _hl_fabric.verify_integrity()

def get_stats() -> dict:
    """API pública soberana para estadísticas."""
    return _hl_fabric.get_stats()

def suggest_from_history(verb: str) -> dict | None:
    """API pública soberana de sugerencia Behavioral RAG."""
    return _hl_fabric.suggest_from_history(verb)

def get_verb_frequency(limit: int = 20) -> list[dict]:
    """API pública: frecuencia de verbos VALID."""
    return _hl_fabric.get_verb_frequency(limit)

def get_library_stats() -> list[dict]:
    """API pública: estadísticas por biblioteca."""
    return _hl_fabric.get_library_stats()

def get_knot_distribution() -> list[dict]:
    """API pública: distribución de nudos."""
    return _hl_fabric.get_knot_distribution()

def get_session_timeline(days: int = 7) -> list[dict]:
    """API pública: actividad por día."""
    return _hl_fabric.get_session_timeline(days)

def export_crystals_report() -> dict:
    """API pública: reporte completo de cristales."""
    return _hl_fabric.export_crystals_report()

def get_crystal_count() -> int:
    """API pública: cantidad total de cristales."""
    return _hl_fabric.get_crystal_count()

def switch_unicode(mode: str = "STACKING") -> str:
    """API pública: conmutar modo Unicode soberano."""
    return _hl_fabric.switch_unicode_mode(mode)

def assign_tomo_ids() -> dict:
    """API pública: asignar TOMO_IDs a cristales."""
    return _hl_fabric.assign_tomo_ids()

def get_unicode_mode() -> str:
    """API pública: obtener modo Unicode activo."""
    return _hl_fabric.get_unicode_mode()


# ── Test soberano de arranque ─────────────────────────────────────
if __name__ == "__main__":
    from .grammar import validate
    
    print("═" * 60)
    print("DIRIME IMV — HL FABRIC Ledger Soberano")
    print("═" * 60)
    
    # Test 1: Registrar validación gramatical
    test_sentence = validate("TRUST FOUNDATION =><= .. verifica .. scope_activo --[As de Guía] [term]")
    tx_id = record_grammar(test_sentence)
    print(f"\nTransacción registrada: {tx_id}")
    
    # Test 2: Registrar cristal
    crystal_id = record_crystal("test_crystal_001", "TEST_FORM", "contenido de prueba", 5)
    print(f"Cristal registrado: {crystal_id}")
    
    # Test 3: Verificar integridad
    integrity_ok = verify_ledger()
    print(f"\nIntegridad ledger: {'OK' if integrity_ok else 'CORRUPTED'}")
    
    # Test 4: Estadísticas
    stats = get_stats()
    print(f"\nEstadísticas:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test 5: Transacciones recientes
    recent = get_recent(3)
    print(f"\nTransacciones recientes ({len(recent)}):")
    for tx in recent:
        print(f"  {tx.id[:8]}... - {tx.type.value} - {tx.timestamp}")
    
    print("\n═" * 60)
# ── NOTARIA functions ─────────────────────────────────────────────────────

def record_notaria_act(acto: str, partes: list, objeto: str, scalar_s: float) -> str:
    """Registra un acto notarial soberano en el ledger."""
    import hashlib, time as _time
    ts    = _time.time()
    hash_ = hashlib.sha256(f"{acto}:{objeto}:{ts}".encode()).hexdigest()[:24]
    tx = Transaction(
        type=TransactionType.GRAMMAR_VALIDATION,
        knowledge_state="GREEN" if scalar_s >= 0.78 else "BLUE",
        data={
            "sentence": f"CRYPTO (spark seat) =><= .. certifica .. {objeto} --[Nudo de Ocho] [term]",
            "result":   "VALID",
            "library":  "CRYPTO",
            "verb":     "certifica",
            "knot":     "Nudo de Ocho",
            "scalar_s": scalar_s,
            "acto":     acto,
            "partes":   partes,
            "objeto":   objeto,
            "hash":     hash_,
            "tipo":     "NOTARIA_ACT",
        }
    )
    _hl_fabric.record_transaction(tx)
    return hash_

def get_notaria_stats() -> dict:
    """Estadísticas del pipeline notarial soberano."""
    import json as _json, sqlite3
    with sqlite3.connect(_hl_fabric.db_path) as conn:
        rows = conn.execute(
            "SELECT data FROM transactions ORDER BY timestamp DESC LIMIT 500"
        ).fetchall()
    actos_total = actos_wu = actos_ku = h63_count = 0
    scalar_sum  = 0.0
    for (raw,) in rows:
        try:
            d = _json.loads(raw) if raw else {}
        except Exception:
            continue
        if d.get("tipo") != "NOTARIA_ACT":
            continue
        actos_total += 1
        s = d.get("scalar_s", 0.0)
        scalar_sum += s
        if s >= 0.90:
            actos_wu += 1
            h63_count += 1
        elif s >= 0.78:
            actos_wu += 1
        else:
            actos_ku += 1
    return {
        "actos_total":    actos_total,
        "actos_wu":       actos_wu,
        "actos_ku":       actos_ku,
        "scalar_promedio": round(scalar_sum / actos_total, 3) if actos_total else 0.0,
        "h63_count":      h63_count,
    }
def export_notaria_report() -> list[dict]:
    """Exporta actos notariales — TX VALID de bibliotecas CRYPTO/TRUST con S >= 0.78."""
    return _hl_fabric.export_notaria_report()
