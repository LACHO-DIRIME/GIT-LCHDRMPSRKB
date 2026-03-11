"""
ELPULSAR — core/resources.py
Gestión de recursos soberanos: propios/ajenos · internos/externos.
Referencia: BIBLIO-SOURCES(ELPULSAR).txt §2.3
"""
from __future__ import annotations
import sqlite3, json, time, uuid
from pathlib import Path
from enum import Enum

_DB = Path(__file__).parent.parent.parent.parent / "IMV" / "data" / "sovereign.db"

class ResourceType(Enum):
    LACHO = "LACHO"
    DATA  = "DATA"
    REF   = "REF"
    CODE  = "CODE"
    LINK  = "LINK"

class ResourceScope(Enum):
    PROPIO   = "PROPIO"
    AJENO    = "AJENO"
    INTERNO  = "INTERNO"
    EXTERNO  = "EXTERNO"

def _init_db():
    with sqlite3.connect(_DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS elpulsar_resources (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                type TEXT NOT NULL,
                scope TEXT NOT NULL,
                content TEXT,
                tomo_id TEXT,
                cluster TEXT,
                verified INTEGER DEFAULT 0,
                created_at REAL,
                updated_at REAL
            )""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS elpulsar_connections (
                id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                relation TEXT NOT NULL,
                weight REAL DEFAULT 1.0,
                created_at REAL
            )""")
        conn.commit()

def create(title, type, scope, content="",
           tomo_id=None, cluster="#CORE"):
    _init_db()
    r = {"id": str(uuid.uuid4())[:8], "title": title,
         "type": type.value, "scope": scope.value,
         "content": content, "tomo_id": tomo_id,
         "cluster": cluster, "verified": 0,
         "created_at": time.time(), "updated_at": time.time()}
    with sqlite3.connect(_DB) as conn:
        # Si ya existe mismo título+tipo+scope — retornar existente
        existing = conn.execute(
            "SELECT * FROM elpulsar_resources "
            "WHERE title=? AND type=? AND scope=?",
            (title, type.value, scope.value)).fetchone()
        if existing:
            return dict(zip([
                "id","title","type","scope","content",
                "tomo_id","cluster","verified",
                "created_at","updated_at"], existing))
        conn.execute("""INSERT INTO elpulsar_resources
            (id,title,type,scope,content,tomo_id,cluster,
             verified,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)""", tuple(r.values()))
        conn.commit()
    return r

def get_all(cluster=None, scope=None):
    _init_db()
    with sqlite3.connect(_DB) as conn:
        conn.row_factory = sqlite3.Row
        q = "SELECT * FROM elpulsar_resources WHERE 1=1"
        p = []
        if cluster: q += " AND cluster=?"; p.append(cluster)
        if scope:   q += " AND scope=?";   p.append(scope)
        q += " ORDER BY updated_at DESC"
        return [dict(r) for r in conn.execute(q, p).fetchall()]

def verify(resource_id):
    with sqlite3.connect(_DB) as conn:
        n = conn.execute(
            "UPDATE elpulsar_resources SET verified=1,"
            "updated_at=? WHERE id=?",
            (time.time(), resource_id)).rowcount
        conn.commit()
    return n > 0

def connect(source_id, target_id,
            relation="DEPENDE_DE", weight=1.0):
    _init_db()
    c = {"id": str(uuid.uuid4())[:8],
         "source_id": source_id, "target_id": target_id,
         "relation": relation, "weight": weight,
         "created_at": time.time()}
    with sqlite3.connect(_DB) as conn:
        conn.execute("""INSERT INTO elpulsar_connections
            (id,source_id,target_id,relation,weight,created_at)
            VALUES (?,?,?,?,?,?)""", tuple(c.values()))
        conn.commit()
    return c

def get_connections(resource_id=None):
    _init_db()
    with sqlite3.connect(_DB) as conn:
        conn.row_factory = sqlite3.Row
        if resource_id:
            rows = conn.execute("""SELECT * FROM elpulsar_connections
                WHERE source_id=? OR target_id=?""",
                (resource_id, resource_id)).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM elpulsar_connections").fetchall()
    return [dict(r) for r in rows]

def deduplicate():
    """Elimina recursos duplicados — conserva el más antiguo."""
    with sqlite3.connect(_DB) as conn:
        conn.execute("""
            DELETE FROM elpulsar_resources
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM elpulsar_resources
                GROUP BY title, type, scope
            )""")
        conn.commit()
    return len(get_all())

def sync_from_ledger(db_path=None):
    """Sincroniza cristales→LACHO y tareas scheduler→DATA en TABLE."""
    import time as _t
    from pathlib import Path as _P
    if db_path is None:
        db_path = _DB
    if not _P(str(db_path)).exists():
        return {"crystals": 0, "tasks": 0}
    _init_db()
    sc = st = 0
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        for row in conn.execute(
            "SELECT id,form,content,frequency,tomo_id FROM crystals ORDER BY frequency DESC"
        ).fetchall():
            rid = f"cr_{row['id']}"
            if not conn.execute(
                "SELECT id FROM elpulsar_resources WHERE id=?",(rid,)
            ).fetchone():
                conn.execute("""INSERT OR IGNORE INTO elpulsar_resources
                    (id,title,type,scope,content,tomo_id,cluster,verified,created_at,updated_at)
                    VALUES(?,?,?,?,?,?,?,?,?,?)""",
                    (rid,(row["form"] or "")[:40],"LACHO","PROPIO",
                     row["content"] or row["form"],row["tomo_id"],
                     "#STACKING",1,_t.time(),_t.time()))
                sc += 1
        conn.commit()
    sdb = _P(__file__).parent.parent.parent.parent/"DIRIME_v2"/"scheduler"/"scheduler.db"
    if sdb.exists():
        try:
            with sqlite3.connect(sdb) as s:
                s.row_factory = sqlite3.Row
                tareas = s.execute(
                    "SELECT * FROM tareas ORDER BY created_at DESC LIMIT 50"
                ).fetchall()
            with sqlite3.connect(db_path) as conn:
                for t in tareas:
                    rid = f"sc_{t['id']}"
                    if not conn.execute(
                        "SELECT id FROM elpulsar_resources WHERE id=?",(rid,)
                    ).fetchone():
                        conn.execute("""INSERT OR IGNORE INTO elpulsar_resources
                            (id,title,type,scope,content,cluster,verified,created_at,updated_at)
                            VALUES(?,?,?,?,?,?,?,?,?)""",
                            (rid,t["titulo"][:40],"DATA","INTERNO",t["estado"],
                             t.get("cluster","#CORE"),
                             1 if t["estado"]=="UF[H63]" else 0,
                             t["created_at"],t["created_at"]))
                        st += 1
                conn.commit()
        except: pass
    return {"crystals": sc, "tasks": st}

if __name__ == "__main__":
    # Limpiar duplicados existentes
    n = deduplicate()
    print(f"Recursos tras deduplicar: {n}")
    print(f"Conexiones: {len(get_connections())}")
    print("✅ resources.py ok")
