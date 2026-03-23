#!/usr/bin/env python3
"""
DIRIME — create_fri_notaria_db.py
Crea base de datos NOTARIA KALIL para viernes 13/03.

Referencia: sovereign.db schema del proyecto
"""

import sqlite3
import os
from pathlib import Path

def create_fri_notaria_db():
    """Crea base de datos NOTARIA KALIL con schema soberano."""
    
    # Ruta de la base de datos
    db_path = Path(__file__).parent / "$fri.CORPUS_NOTARIA_KALIL.MU-STORE.db"
    
    # Eliminar si existe para crear fresca
    if db_path.exists():
        db_path.unlink()
    
    # Crear conexión
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Crear tabla transactions (schema existente)
    cursor.execute("""
        CREATE TABLE transactions (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            timestamp REAL NOT NULL,
            data TEXT NOT NULL,
            hash TEXT,
            verified BOOLEAN DEFAULT FALSE,
            created_at REAL DEFAULT (strftime('%s', 'now'))
        )
    """)
    
    # Crear tabla mu_store (schema existente)
    cursor.execute("""
        CREATE TABLE mu_store (
            id INTEGER PRIMARY KEY,
            hexagrama TEXT NOT NULL,
            verbo TEXT NOT NULL,
            biblioteca TEXT NOT NULL,
            scalar_threshold REAL DEFAULT 0.88,
            estado TEXT DEFAULT 'KU',
            descripcion TEXT,
            ancla_rag TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insertar registros mu_store para NOTARIA KALIL
    mu_store_data = [
        (None, 'H63', 'hash', 'CRYPTO', 0.93, 'WU', 'hash acto en blockchain', 'BOLIVAR =><= .. hashea .. acto_notarial --[Nudo de Ocho] [term]'),
        (None, 'H63', 'evalua', 'METHOD', 0.88, 'WU', 'rating partes del acto', 'NORA =><= .. evalua .. rating_partes --[As de Guía] [term]'),
        (None, 'H63', 'calcula', 'METHOD', 0.85, 'KU', 'tarifa notarial pendiente', 'CARILO =><= .. calcula .. tarifa_notarial --[As de Guía] [term]'),
        (None, 'H05', 'contiene', 'GATE', 0.85, 'KU', 'espera partes reunidas', 'GATE UF[H05] =><= .. contiene .. partes_reunidas --[Ballestrinque] [term]'),
        (None, 'H56', 'penetra', 'ACTIVITY', 0.82, 'KU', 'acto en tránsito', 'ACTIVITY UF[H56] =><= .. penetra .. acto_en_transito --[As de Guía] [term]')
    ]
    
    cursor.executemany("""
        INSERT INTO mu_store (
            id, hexagrama, verbo, biblioteca, scalar_threshold, estado, descripcion, ancla_rag
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, mu_store_data)
    
    # Confirmar cambios
    conn.commit()
    
    # Verificar inserción
    cursor.execute("SELECT COUNT(*) FROM mu_store")
    count = cursor.fetchone()[0]
    
    # Cerrar conexión
    conn.close()
    
    # Imprimir resultado
    print(f"✅ {db_path.name} creado — {count} registros mu_store")
    
    return str(db_path)

if __name__ == "__main__":
    create_fri_notaria_db()
