import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from core.logger import create_logger

logger = create_logger("PERSISTENCE")

class DatabaseManager:
    def __init__(self, db_path="data/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self.init_db()
    
    def init_db(self):
        """Initialize database with required tables"""
        try:
            self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            cursor = self.connection.cursor()
            
            # Short-term memory table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS short_term_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ttl_seconds INTEGER
                )
            ''')
            
            # Episodic memory table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS episodic_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    context TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    importance REAL DEFAULT 1.0
                )
            ''')
            
            # Semantic memory table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS semantic_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    concept TEXT UNIQUE NOT NULL,
                    data TEXT NOT NULL,
                    category TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # User preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    data_type TEXT,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Learned skills table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS learned_skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    implementation TEXT NOT NULL,
                    success_count INTEGER DEFAULT 0,
                    failure_count INTEGER DEFAULT 0,
                    confidence REAL DEFAULT 0.5,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_used DATETIME
                )
            ''')
            
            # Command history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS command_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT NOT NULL,
                    parsed_intent TEXT,
                    extracted_entities TEXT,
                    action_taken TEXT,
                    result TEXT,
                    success BOOLEAN,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    execution_time REAL
                )
            ''')
            
            # Conversation context table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_context (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    user_input TEXT NOT NULL,
                    jarvis_response TEXT NOT NULL,
                    context_data TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Task history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS task_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT NOT NULL,
                    description TEXT,
                    status TEXT,
                    plan TEXT,
                    result TEXT,
                    error TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME
                )
            ''')
            
            # Backup log table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS backup_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    backup_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    backup_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    size_bytes INTEGER
                )
            ''')
            
            self.connection.commit()
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """Insert record into table"""
        try:
            cursor = self.connection.cursor()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = list(data.values())
            
            cursor.execute(
                f'INSERT INTO {table} ({columns}) VALUES ({placeholders})',
                values
            )
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Error inserting into {table}: {e}")
            return -1
    
    def update(self, table: str, data: Dict[str, Any], where: str) -> bool:
        """Update records in table"""
        try:
            cursor = self.connection.cursor()
            set_clause = ', '.join([f'{k}=?' for k in data.keys()])
            values = list(data.values())
            
            cursor.execute(
                f'UPDATE {table} SET {set_clause} WHERE {where}',
                values
            )
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating {table}: {e}")
            return False
    
    def select(self, table: str, where: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
        """Select records from table"""
        try:
            cursor = self.connection.cursor()
            query = f'SELECT * FROM {table}'
            if where:
                query += f' WHERE {where}'
            if limit:
                query += f' LIMIT {limit}'
            
            cursor.execute(query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Error selecting from {table}: {e}")
            return []
    
    def select_one(self, table: str, where: str) -> Optional[Dict]:
        """Select single record from table"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'SELECT * FROM {table} WHERE {where}')
            columns = [description[0] for description in cursor.description]
            row = cursor.fetchone()
            
            return dict(zip(columns, row)) if row else None
        except Exception as e:
            logger.error(f"Error selecting from {table}: {e}")
            return None
    
    def delete(self, table: str, where: str) -> bool:
        """Delete records from table"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'DELETE FROM {table} WHERE {where}')
            self.connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting from {table}: {e}")
            return False
    
    def execute_custom(self, query: str, params: Optional[Tuple] = None) -> List[Dict]:
        """Execute custom SQL query"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            columns = [description[0] for description in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            
            return [dict(zip(columns, row)) for row in rows] if columns else []
        except Exception as e:
            logger.error(f"Error executing custom query: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


_db_instance = None

def get_database() -> DatabaseManager:
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance
