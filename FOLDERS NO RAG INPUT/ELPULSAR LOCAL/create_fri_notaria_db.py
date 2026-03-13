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
    
    # Crear tabla transactions (schema soberano)
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
    
    # Crear tabla mu_store (schema soberano)
    cursor.execute("""
        CREATE TABLE mu_store (
            id TEXT PRIMARY KEY,
            hexagrama TEXT NOT NULL,
            clave TEXT NOT NULL,
            tipo TEXT NOT NULL,
            scalar REAL NOT NULL,
            estado TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            ancla_rag TEXT
        )
    """)
    
    # Insertar registros mu_store para NOTARIA KALIL
    mu_store_data = [
        ('ms001', 'H63', 'BOLIVAR_HASH',  'CRYPTO',   0.93, 'WU', 'hash acto en blockchain',      'BOLIVAR =><= .. hashea .. acto_notarial --[Nudo de Ocho] [term]'),
        ('ms002', 'H63', 'NORA_PARTES',   'METHOD',   0.88, 'WU', 'rating partes del acto',       'NORA =><= .. evalua .. rating_partes --[As de Guía] [term]'),
        ('ms003', 'H63', 'CARILO_FEE',    'METHOD',   0.85, 'KU', 'tarifa notarial pendiente',     'CARILO =><= .. calcula .. tarifa_notarial --[As de Guía] [term]'),
        ('ms004', 'H05', 'GATE_ACTO',     'GATE',     0.85, 'KU', 'espera partes reunidas',        'GATE UF[H05] =><= .. contiene .. partes_reunidas --[Ballestrinque] [term]'),
        ('ms005', 'H56', 'VIAJERO_ACTO',  'ACTIVITY', 0.82, 'KU', 'acto en tránsito',              'ACTIVITY UF[H56] =><= .. penetra .. acto_en_transito --[As de Guía] [term]')
    ]
    
    cursor.executemany("""
        INSERT INTO mu_store (
            id, hexagrama, clave, tipo, scalar, estado, descripcion, ancla_rag
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
