#!/bin/bash

# Backup current state

echo "Creating backup..."
mkdir -p data/backups

BACKUP_DIR="data/backups/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "Backing up core files..."
cp -r core "$BACKUP_DIR/"
cp -r brain "$BACKUP_DIR/"
cp -r planner "$BACKUP_DIR/"
cp -r agent "$BACKUP_DIR/"
cp -r tools "$BACKUP_DIR/"
cp -r skills "$BACKUP_DIR/"
cp -r security "$BACKUP_DIR/"
cp -r scheduler "$BACKUP_DIR/"
cp -r memory "$BACKUP_DIR/"
cp -r config "$BACKUP_DIR/"
cp -r data/memory.db "$BACKUP_DIR/" 2>/dev/null || true

echo "Backup created at: $BACKUP_DIR"
echo "Total size: $(du -sh $BACKUP_DIR | cut -f1)"
