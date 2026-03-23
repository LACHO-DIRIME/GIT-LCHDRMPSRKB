#!/bin/bash
# DIRIME BACKUP PROTOCOL — backup.sh
# Ejecutar desde: /media/Personal/CLUSTER-FERIA_SUN22-03/LACHO_NEXT_STEP/DIRIME_old_repo/DIRIME
# Uso: bash MAINTENANCE/backup.sh

set -e

# Auto-detectar raíz del repo
DIRIME_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

SOVEREIGN_DB="$DIRIME_ROOT/IMV/data/sovereign.db"
BACKUP_DB="$DIRIME_ROOT/IMV/data/sovereign.db.backup_$(date +%Y%m%d_%H%M)"
BACKUP_LOG="$DIRIME_ROOT/MAINTENANCE/backup.log"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

echo "=== DIRIME BACKUP PROTOCOL ==="
echo "Timestamp: $TIMESTAMP"
echo "Root: $DIRIME_ROOT"
echo ""

# STEP 1: Backup sovereign.db
echo "[1/3] Backing up sovereign.db..."
if [ -f "$SOVEREIGN_DB" ]; then
    if command -v sqlite3 &>/dev/null; then
        sqlite3 "$SOVEREIGN_DB" ".backup $BACKUP_DB"
        echo "      OK (sqlite3): $BACKUP_DB"
    else
        # Fallback: simple file copy
        cp "$SOVEREIGN_DB" "$BACKUP_DB"
        echo "      OK (cp): $BACKUP_DB"
    fi
else
    echo "      WARN: sovereign.db not found — skipping DB backup"
fi

# STEP 2: Integrity check
echo "[2/3] Integrity check..."
if [ -f "$SOVEREIGN_DB" ]; then
    if command -v sqlite3 &>/dev/null; then
        INTEGRITY=$(sqlite3 "$SOVEREIGN_DB" "PRAGMA integrity_check;" 2>/dev/null || echo "error")
        if [ "$INTEGRITY" = "ok" ]; then
            echo "      OK: integrity check passed"
        else
            echo "      WARN: integrity check returned: $INTEGRITY"
        fi
    else
        echo "      SKIP: sqlite3 not installed — install with: sudo apt install sqlite3"
    fi
else
    echo "      SKIP: no DB to check"
fi

# STEP 3: Log backup
echo "[3/3] Logging..."
mkdir -p "$(dirname "$BACKUP_LOG")"
echo "$TIMESTAMP | BACKUP_OK | root=$DIRIME_ROOT" >> "$BACKUP_LOG"
echo "      OK: $BACKUP_LOG"

# Limpiar backups viejos (conservar últimos 5)
ls -t "$DIRIME_ROOT/IMV/data/sovereign.db.backup_"* 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true

echo ""
echo "=== BACKUP COMPLETE ==="
