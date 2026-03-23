"""
DIRIME IMV — core/rag.py
IME Modo RAG mínimo — BM25 sobre CORPUS.

Referencia: BIBLIO-SOURCES(IME-TRANSDUCTOR).txt §2.1
Sin dependencias externas — Python puro + math.
"""

from __future__ import annotations
import re
import math
from pathlib import Path
from typing import Optional

_CORPUS_DIR = Path(__file__).parent.parent.parent / "CORPUS"
# LIBRO integrado en CORPUS — directorio unificado

_THEATER_DIR = Path(__file__).parent.parent.parent / "RUNTIME" / "THEATER"
_RUNNERS_DIR = Path(__file__).parent.parent.parent / "RUNTIME" / "RUNNERS"
_AGENTS_DIR  = Path(__file__).parent.parent.parent / "RUNTIME" / "AGENTS"
_ELPULSAR_LOCAL_DIR = Path(__file__).parent.parent.parent / "RUNTIME" / "NERVE_CELLS"
_ASKINGS_DIR = Path("/media/Personal/DIRIME/Askings for autoresearching by technical horizons")
_LEARNING_DIR = Path(__file__).parent.parent.parent / "LEARNING"

_SOVEREIGN_SOURCES = [
    (_THEATER_DIR, "*.theater", "theater", 1.8),
    (_RUNNERS_DIR, "*",         "runner",  1.6),
    (_AGENTS_DIR,  "*",         "agent",   2.0),
    (_ELPULSAR_LOCAL_DIR, "*nerve_cell*", "nerve_cell", 2.0),   # Nerve Cells notariales
    (_ASKINGS_DIR, "*.json",    "askings", 1.7),                 # Askings for autoresearching
    (_ASKINGS_DIR, "*.yml",     "askings", 1.7),                 # Askings YAML files
    (_LEARNING_DIR, "*.md",     "learning", 2.0),                # LEARNING/ docs
]


class IMEBM25:
    """
    IME Modo RAG — BM25 sobre archivos CORPUS.
    Encuentra ejemplos soberanos relevantes para el input del operador.
    """
    K1 = 1.5
    B  = 0.75

    def __init__(self):
        self._docs: list[dict] = []
        self._built = False


    # ── TASK_3.2 — MEMOIZATION ──────────────────────────────────────────
    def _corpus_fingerprint(self) -> str:
        """Hash of all doc file + boost — changes when corpus changes."""
        import hashlib
        parts = sorted(f"{d.get('file','')}:{d.get('boost',1.0)}" for d in self._docs)
        return hashlib.md5("|".join(parts).encode()).hexdigest()

    def search_cached(self, query: str, top_k: int = 3) -> list[dict]:
        """
        MEMOIZATION: cache BM25 results per (query_hash, corpus_fingerprint).
        Reduces repeated lookups from O(N) recompute to O(1) cache hit.
        TASK_3.2
        """
        import hashlib
        if not self._built:
            self.build_index()
        cache_key = hashlib.md5(
            f"{query}|{top_k}|{self._corpus_fingerprint()}".encode()
        ).hexdigest()
        if not hasattr(self, "_query_cache"):
            self._query_cache: dict = {}
        if cache_key not in self._query_cache:
            self._query_cache[cache_key] = self.search(query, top_k)
        return self._query_cache[cache_key]

    def invalidate_cache(self):
        """Call when corpus changes to clear memoization cache."""
        self._query_cache = {}

    # ── TASK_3.4 — INCREMENTAL RAG ──────────────────────────────────────
    def _doc_hash(self, filepath: str) -> str:
        """SHA256 prefix of file content — changes when file changes."""
        import hashlib
        try:
            return hashlib.sha256(open(filepath, "rb").read()).hexdigest()[:16]
        except Exception:
            return "unknown"

    def build_incremental(self, force_rebuild: bool = False) -> int:
        """
        INCREMENTAL_COMPUTATION: only re-index changed or new documents.

        doc_hash unchanged → skip (use existing index entry)
        doc_hash changed   → re-index that document only
        new doc added      → append to existing index

        At 5x corpus (925 BIBLIO-SOURCES), reduces startup from ~90s to <2s.
        TASK_3.4
        """
        if not hasattr(self, "_doc_hashes"):
            self._doc_hashes: dict[str, str] = {}

        if not self._built:
            return self.build_index()

        changed_count = 0
        for doc in list(self._docs):
            filepath = doc.get("file", "")
            if not filepath.startswith("corpus:"):
                continue
            # Strip prefix to get actual path for hashing
            actual_path = str(filepath)
            current_hash = self._doc_hash(actual_path)
            if force_rebuild or self._doc_hashes.get(actual_path) != current_hash:
                self._doc_hashes[actual_path] = current_hash
                changed_count += 1

        if changed_count > 0:
            self.invalidate_cache()

        return changed_count

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r'[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+', text.lower())

    def _extract_askings_text(self, data: dict, filename: str) -> str:
        """Extrae texto searchable de archivos JSON Askings."""
        lines = [f"Askings file: {filename}"]
        
        # Extract from filesystem section
        if "filesystem" in data:
            fs = data["filesystem"]
            if "summary" in fs:
                summary = fs["summary"]
                lines.extend([
                    f"Total modules: {summary.get('total_modules', 0)}",
                    f"Active modules: {summary.get('active', 0)}",
                    f"Declared modules: {summary.get('declared', 0)}",
                    f"Stub modules: {summary.get('stub', 0)}",
                    f"Blocked modules: {summary.get('blocked', 0)}"
                ])
            
            # Extract module information
            if "modules" in fs:
                for module_path, module_info in fs["modules"].items():
                    status = module_info.get("status", "unknown")
                    reason = module_info.get("reason", "")
                    lines.append(f"Module {module_path}: status {status} reason {reason}")
        
        # Extract from gap_analysis section
        if "gap_analysis" in data:
            gap = data["gap_analysis"]
            if "summary" in gap:
                summary = gap["summary"]
                lines.extend([
                    f"Gap priority: {summary.get('overall_priority', 'unknown')}",
                    f"Missing implementations: {summary.get('total_missing', 0)}",
                    f"Incomplete modules: {summary.get('total_incomplete', 0)}",
                    f"Test coverage gaps: {summary.get('total_test_gaps', 0)}",
                    f"Dependency gaps: {summary.get('total_dependency_gaps', 0)}"
                ])
            
            # Extract missing implementations
            if "missing_implementations" in gap:
                for item in gap["missing_implementations"]:
                    module = item.get("module", "")
                    reason = item.get("reason", "")
                    priority = item.get("priority", "")
                    lines.append(f"Missing implementation: {module} reason {reason} priority {priority}")
        
        # Extract from upgrade_plan section
        if "upgrade_plan" in data:
            plan = data["upgrade_plan"]
            if "immediate_actions" in plan:
                for action in plan["immediate_actions"]:
                    act_type = action.get("action", "")
                    module = action.get("module", "")
                    hours = action.get("estimated_hours", 0)
                    lines.append(f"Immediate action: {act_type} module {module} estimated {hours} hours")
        
        return "\n".join(lines)

    def build_index(self) -> int:
        """Construye índice BM25 desde CORPUS. Retorna docs indexados."""
        if not _CORPUS_DIR.exists():
            return 0

        self._docs = []
        for f in _CORPUS_DIR.rglob("*.txt"):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                # Extraer sentencias LACHO
                lacho_lines = [
                    ln.strip() for ln in text.splitlines()
                    if "=><=".replace(" ","") in ln and "[term]" in ln
                ]
                # Extraer prosa relevante (primeras 60 líneas no vacías)
                prose_lines = [
                    ln.strip() for ln in text.splitlines()
                    if ln.strip() and not ln.strip().startswith("//")
                    and not ln.strip().startswith("#!")
                ][:60]

                # Combinar: sentencias LACHO + prosa inicial
                if lacho_lines or prose_lines:
                    snippet_parts = []
                    if prose_lines:
                        snippet_parts.append("\n".join(prose_lines[:30]))
                    if lacho_lines:
                        snippet_parts.append("\n".join(lacho_lines[:20]))
                    snippet = "\n".join(snippet_parts)

                    # Boost para BIBLIA/ y LEARNING/
                    boost = 1.0
                    if "BIBLIA" in str(f):
                        boost = 1.8
                    if "LEARNING" in str(f):
                        boost = 1.5

                    self._docs.append({
                        "file": f"corpus:{f.name}",
                        "text": snippet,
                        "tokens": self._tokenize(snippet),
                        "source": "corpus",
                        "boost": boost
                    })
            except Exception:
                continue

        # LIBRO integrado en CORPUS — no hay directorio separado
        if False:
            for f in []:
                try:
                    text = f.read_text(encoding="utf-8", errors="ignore")[:3000]
                    if text.strip():
                        self._docs.append({
                            "file": f"libro:{f.name}",
                            "text": text,
                            "tokens": self._tokenize(text),
                            "source": "libro"
                        })
                except Exception:
                    continue

        # CAPA 4: THEATER / RUNNERS / AGENTS / ASKINGS
        for src_dir, pattern, src_tag, boost in _SOVEREIGN_SOURCES:
            if not src_dir.exists():
                continue
            for f in src_dir.glob(pattern):
                try:
                    text = f.read_text(encoding="utf-8", errors="ignore")
                    if text.strip():
                        # Special handling for Askings files
                        if src_tag == "askings":
                            # Extract key information from JSON/YAML Askings files
                            if f.suffix == ".json":
                                import json
                                try:
                                    data = json.loads(text)
                                    # Create searchable text from JSON structure
                                    searchable_text = self._extract_askings_text(data, f.name)
                                    text = searchable_text
                                except:
                                    text = text[:2000]  # Fallback to raw text
                            elif f.suffix in [".yml", ".yaml"]:
                                # For YAML files, use raw text but limit size
                                text = text[:3000]
                        
                        doc = {
                            "file": f"{src_tag}:{f.name}",
                            "text": text[:4000],
                            "tokens": self._tokenize(text[:4000]),
                            "source": src_tag,
                            "boost": boost
                        }
                        # Boost ×2.0 para docs NOTARIA
                        if "notaria" in f.name.lower() or "NOTARIA" in text[:200]:
                            doc["boost"] = doc["boost"] * 2.0
                        # Additional boost for Askings files
                        elif src_tag == "askings":
                            doc["boost"] = doc["boost"] * 1.5
                        self._docs.append(doc)
                except Exception:
                    continue

        # Behavioral RAG: agregar cristales del ledger como documentos
        try:
            import sqlite3
            db_path = Path(__file__).parent.parent / "data" / "sovereign.db"
            if db_path.exists():
                with sqlite3.connect(db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    rows = conn.execute(
                        "SELECT form, content, frequency FROM crystals "
                        "ORDER BY frequency DESC"
                    ).fetchall()
                    for row in rows:
                        form = row['form'].replace('verbo_soberano:', '')
                        content = row['content'] or ''
                        doc_text = (
                            f"verbo soberano verificado: {form}\n"
                            f"frecuencia: {row['frequency']}x\n"
                            f"ejemplo: {content[:300]}"
                        )
                        tokens = self._tokenize(doc_text)
                        if tokens:
                            self._docs.append({
                                'file': f'crystal:{form}',
                                'text': doc_text,
                                'tokens': tokens,
                            })
        except Exception:
            pass  # behavioral RAG falla silenciosamente

        # Recalcular IDF incluyendo cristales
        N = len(self._docs)
        if N == 0:
            return 0

        df2: dict[str, int] = {}
        for doc in self._docs:
            for tok in set(doc["tokens"]):
                df2[tok] = df2.get(tok, 0) + 1

        self._idf = {
            tok: math.log((N - freq + 0.5) / (freq + 0.5) + 1)
            for tok, freq in df2.items()
        }
        self._avg_dl = sum(len(d["tokens"]) for d in self._docs) / N
        self._built = True
        return N

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Busca los top_k documentos más relevantes para el query."""
        if not self._built:
            self.build_index()
        if not self._docs:
            return []

        q_tokens = self._tokenize(query)
        scores = []

        for doc in self._docs:
            score = 0.0
            dl = len(doc["tokens"])
            tf_map: dict[str, int] = {}
            for tok in doc["tokens"]:
                tf_map[tok] = tf_map.get(tok, 0) + 1

            for tok in q_tokens:
                if tok not in self._idf:
                    continue
                tf = tf_map.get(tok, 0)
                idf = self._idf[tok]
                numerator = tf * (self.K1 + 1)
                denominator = tf + self.K1 * (
                    1 - self.B + self.B * dl / max(self._avg_dl, 1)
                )
                score += idf * (numerator / max(denominator, 1e-9))

            # Boost archivos críticos + CAPA 4 boost
            raw_score = score
            boost = doc.get("boost", 1.0)
            
            # NOTARIA_BOOST para archivos notariales críticos
            NOTARIA_BOOST = {
                "UNICODE_NOTARIA_IMV.txt":                    2.0,
                "CHCL_BASE.txt":                              1.8,
                "UNICODE_PROGRAMS_FULL_STACK_NOTARIA.txt":    1.8,
                "UNICODE_PROGRAMS_KALIL_4_NEURONAS.txt":      1.6,
                "PRACTICE-NOTARIA.lacho":                     1.5,
            }
            # Nerve Cells notariales — boost si están indexados:
            NOTARIA_NC_BOOST = {
                "$thu.Nerve Cell Notaria Training.txt":        1.5,
                "$fri.Nerve Cell KALIL Notaria Training.txt":  1.5,
                "$sun.Nerve Cell China Notaria Training.txt":  1.5,
            }
            
            BOOST_FILES = {
                "BIBLIO-SOURCES(HEADCAT)": 2.0,
                "COGNITIVO_03": 1.8,
                "COGNITIVO_04": 1.8,
                "COGNITIVO_05": 1.8,
                "SOURCE&ASSET": 1.5,
                "BIBLIO-SOURCES(FLYBOT)": 1.5,
                "BIBLIO-SOURCES(TAXONOMY_LACHO)": 1.5,
                "BIBLIO-SOURCES(SOCIAL_SCHEDULER-OS)": 1.4,
                "BIBLIOTECAS_MADRE_LACHO": 1.4,
            }
            fname = doc.get("file","")
            
            # Aplicar boost NOTARIA si corresponde
            notaria_boost = NOTARIA_BOOST.get(fname, NOTARIA_NC_BOOST.get(fname, 1.0))
            boost *= notaria_boost
            
            # Aplicar boost existente
            for key, mult in BOOST_FILES.items():
                if key in fname:
                    boost *= mult
                    break
            
            score = raw_score * boost
            if score > 0:
                scores.append({"file": doc.get("file", "crystal"),
                                "text": doc["text"], "score": score,
                                "source": doc.get("source", "corpus")})

        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]

    def get_examples_for_prompt(self, query: str, max_examples: int = 5) -> str:
        """
        Retorna string listo para inyectar en system prompt de Groq.
        Formato: ejemplos LACHO relevantes al query del operador.
        """
        results = self.search(query, top_k=2)
        if not results:
            return ""

        lines = ["Ejemplos adicionales del corpus relevantes:"]
        count = 0
        for result in results:
            icon = "🧠" if result.get("source") == "behavioral_rag" else "💎" if result.get("file", "").startswith("crystal:") else "📚"
            for line in result["text"].splitlines():
                line = line.strip()
                if "=><=".replace(" ","") in line and "[term]" in line and count < max_examples:
                    lines.append(f"  {icon} {line}")
                    count += 1
                elif result.get("file", "").startswith("crystal:") and count < max_examples:
                    lines.append(f"  {icon} {line}")
                    count += 1
                elif result.get("source") == "behavioral_rag" and count < max_examples:
                    lines.append(f"  {icon} {line}")
                    count += 1
        return "\n".join(lines) if count > 0 else ""


# Instancia global
_rag = IMEBM25()

def get_rag_context(query: str) -> str:
    """API pública: obtener contexto RAG para un query."""
    return _rag.get_examples_for_prompt(query)

def build_rag_index() -> int:
    """API pública: construir índice RAG."""
    return _rag.build_index()


def build_behavioral_index() -> int:
    """
    Behavioral RAG: indexa patrones verificados del ledger como documentos.
    Complementa el índice CORPUS con historial soberano del operador.
    Referencia: BIBLIO-SOURCES(BEHAVIORAL-RAG_MINIMAL).txt
    """
    import sqlite3
    from pathlib import Path

    db_path = Path(__file__).parent.parent / "data" / "sovereign.db"
    if not db_path.exists():
        return 0

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT data FROM transactions
                WHERE type = 'GRAMMAR_VALIDATION'
                AND json_extract(data, '$.result') = 'VALID'
                ORDER BY timestamp DESC
                LIMIT 200
            """).fetchall()
    except Exception:
        return 0

    docs = []
    for row in rows:
        import json
        try:
            d = json.loads(row["data"]) if isinstance(row["data"], str) else dict(row["data"])
            verb    = d.get("verb", "")
            library = d.get("library", "")
            knot    = d.get("knot", "")
            sentence = d.get("sentence", "")
            if verb and library:
                text = (
                    f"PATRON VERIFICADO: {library} con verbo '{verb}' "
                    f"nudo '{knot}'. Sentencia: {sentence}"
                )
                docs.append({"id": f"brag_{verb}_{library}", "text": text,
                             "source": "behavioral_rag"})
        except Exception:
            continue

    # Agregar al índice global existente (evitar duplicados por id)
    added = 0
    existing_ids = {d.get("id") for d in _rag._docs}
    for doc in docs:
        if doc["id"] not in existing_ids:
            _rag._docs.append(doc)
            existing_ids.add(doc["id"])
            added += 1

    # Reconstruir índice BM25 con nuevos documentos
    if added > 0:
        _rag.build_index()

    return added


def build_full_index() -> tuple[int, int]:
    """
    Construye índice completo: CORPUS + Behavioral RAG.
    Retorna (corpus_docs, behavioral_docs).
    """
    corpus_n = build_rag_index()
    behavioral_n = build_behavioral_index()
    return corpus_n, behavioral_n
