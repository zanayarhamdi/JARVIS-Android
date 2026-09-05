#!/bin/bash

# JARVIS-Android Installation Script for Termux

echo "================================================"
echo "JARVIS-Android Installation"
echo "================================================"

# Check Python version
echo "Checking Python version..."
python3 --version

if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Installing..."
    if command -v apt &> /dev/null; then
        apt update
        apt install python3 python3-pip sqlite3 -y
    else
        echo "Error: apt package manager not found"
        exit 1
    fi
fi

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating data directories..."
mkdir -p data/logs
mkdir -p data/backups
mkdir -p data/skills

echo "Initializing database..."
python3 -c "from memory.persistence import get_database; db = get_database(); print('Database initialized')"

echo "================================================"
echo "Installation complete!"
echo "Run: python3 main.py"
echo "================================================"
