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

_THEATER_DIR = Path(__file__).parent.parent.parent / "FOLDERS NO RAG INPUT" / "THEATER"
_RUNNERS_DIR = Path(__file__).parent.parent.parent / "FOLDERS NO RAG INPUT" / "RUNNERS"
_AGENTS_DIR  = Path(__file__).parent.parent.parent / "FOLDERS NO RAG INPUT" / "AGENTS"

_SOVEREIGN_SOURCES = [
    (_THEATER_DIR, "*.theater", "theater", 1.8),
    (_RUNNERS_DIR, "*",         "runner",  1.6),
    (_AGENTS_DIR,  "*",         "agent",   2.0),
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

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r'[a-záéíóúüñA-ZÁÉÍÓÚÜÑ]+', text.lower())

    def build_index(self) -> int:
        """Construye índice BM25 desde CORPUS. Retorna docs indexados."""
        if not _CORPUS_DIR.exists():
            return 0

        self._docs = []
        for f in _CORPUS_DIR.rglob("*.txt"):
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                # Extraer solo líneas con sentencias LACHO (tienen =><= y [term])
                lacho_lines = [
                    ln.strip() for ln in text.splitlines()
                    if "=><=".replace(" ","") in ln and "[term]" in ln
                ]
                if lacho_lines:
                    snippet = "\n".join(lacho_lines[:20])
                    self._docs.append({
                        "file": f"corpus:{f.name}",
                        "text": snippet,
                        "tokens": self._tokenize(snippet),
                        "source": "corpus"
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

        # CAPA 4: THEATER / RUNNERS / AGENTS
        for src_dir, pattern, src_tag, boost in _SOVEREIGN_SOURCES:
            if not src_dir.exists():
                continue
            for f in src_dir.glob(pattern):
                try:
                    text = f.read_text(encoding="utf-8", errors="ignore")
                    if text.strip():
                        self._docs.append({
                            "file": f"{src_tag}:{f.name}",
                            "text": text[:4000],
                            "tokens": self._tokenize(text[:4000]),
                            "source": src_tag,
                            "boost": boost
                        })
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
