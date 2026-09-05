#!/bin/bash

# JARVIS-Android Rollback Script

if [ $# -eq 0 ]; then
    echo "Usage: ./rollback.sh <backup_directory>"
    echo ""
    echo "Available backups:"
    ls -d data/backups/backup_*/ 2>/dev/null | sed 's|data/backups/||g'
    exit 1
fi

BACKUP_DIR=$1

if [ ! -d "$BACKUP_DIR" ]; then
    echo "Backup not found: $BACKUP_DIR"
    exit 1
fi

echo "Rolling back from: $BACKUP_DIR"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Rollback cancelled."
    exit 0
fi

echo "Restoring files..."
cp -r "$BACKUP_DIR"/core/ .
cp -r "$BACKUP_DIR"/brain/ .
cp -r "$BACKUP_DIR"/planner/ .
cp -r "$BACKUP_DIR"/agent/ .
cp -r "$BACKUP_DIR"/tools/ .
cp -r "$BACKUP_DIR"/skills/ .
cp -r "$BACKUP_DIR"/security/ .
cp -r "$BACKUP_DIR"/scheduler/ .
cp -r "$BACKUP_DIR"/memory/ .
cp -r "$BACKUP_DIR"/config/ .
cp "$BACKUP_DIR"/memory.db data/ 2>/dev/null || true

echo "Rollback complete!"
