"""
Database Manager
Quản lý lưu trữ attempts
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from models import Attempt, AttemptStep, Hint


class DatabaseManager:
    """Quản lý database SQLite"""
    
    def __init__(self, db_path="analyzer.db"):
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        """Khởi tạo database"""
        if not self.db_path.exists():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute("""
                CREATE TABLE attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    problem_id TEXT NOT NULL,
                    original_code TEXT NOT NULL,
                    bug_type TEXT,
                    current_code TEXT,
                    attempt_number INTEGER,
                    hints_viewed TEXT,
                    current_hint_index INTEGER,
                    tests_passed INTEGER DEFAULT 0,
                    tests_total INTEGER,
                    is_solved BOOLEAN DEFAULT 0,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_time TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE attempt_steps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    attempt_id INTEGER NOT NULL,
                    step_number INTEGER,
                    action_type TEXT,
                    code_before TEXT,
                    code_after TEXT,
                    hint_id TEXT,
                    hint_text TEXT,
                    test_results TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (attempt_id) REFERENCES attempts(id)
                )
            """)
            
            conn.commit()
            conn.close()
    
    def save_attempt(self, attempt: Attempt):
        """Lưu attempt mới"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO attempts 
            (user_id, problem_id, original_code, bug_type, current_code, 
             attempt_number, hints_viewed, current_hint_index, tests_passed, 
             tests_total, is_solved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            attempt.user_id,
            attempt.problem_id,
            attempt.original_code,
            attempt.bug_type,
            attempt.current_code,
            attempt.attempt_number,
            json.dumps(attempt.hints_viewed),
            attempt.current_hint_index,
            attempt.tests_passed,
            attempt.tests_total,
            attempt.is_solved
        ))
        
        attempt.id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return attempt.id
    
    def update_attempt(self, attempt: Attempt):
        """Cập nhật attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE attempts
            SET current_code = ?, 
                hints_viewed = ?,
                current_hint_index = ?,
                tests_passed = ?,
                tests_total = ?,
                is_solved = ?,
                last_modified = CURRENT_TIMESTAMP,
                completed_time = ?
            WHERE id = ?
        """, (
            attempt.current_code,
            json.dumps(attempt.hints_viewed),
            attempt.current_hint_index,
            attempt.tests_passed,
            attempt.tests_total,
            attempt.is_solved,
            attempt.completed_time,
            attempt.id
        ))
        
        conn.commit()
        conn.close()
    
    def save_step(self, attempt_id: int, step: AttemptStep):
        """Lưu một step trong attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO attempt_steps
            (attempt_id, step_number, action_type, code_before, code_after, 
             hint_id, hint_text, test_results)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            attempt_id,
            step.step_number,
            step.action_type,
            step.code_before,
            step.code_after,
            step.hint_id,
            step.hint_text,
            json.dumps(step.test_results)
        ))
        
        step.id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return step.id
    
    def get_attempt(self, attempt_id: int) -> dict:
        """Lấy thông tin attempt"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM attempts WHERE id = ?", (attempt_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return dict(row)
    
    def get_attempt_steps(self, attempt_id: int) -> list:
        """Lấy tất cả steps của một attempt"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM attempt_steps WHERE attempt_id = ? ORDER BY step_number",
            (attempt_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_user_attempts(self, user_id: str, problem_id: str = None) -> list:
        """Lấy tất cả attempts của user"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if problem_id:
            cursor.execute(
                "SELECT * FROM attempts WHERE user_id = ? AND problem_id = ? ORDER BY start_time DESC",
                (user_id, problem_id)
            )
        else:
            cursor.execute(
                "SELECT * FROM attempts WHERE user_id = ? ORDER BY start_time DESC",
                (user_id,)
            )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_statistics(self, attempt_id: int) -> dict:
        """Lấy thống kê của 1 attempt"""
        attempt = self.get_attempt(attempt_id)
        steps = self.get_attempt_steps(attempt_id)
        
        if not attempt:
            return None
        
        start_time = datetime.fromisoformat(attempt['start_time'])
        last_modified = datetime.fromisoformat(attempt['last_modified'])
        duration = (last_modified - start_time).total_seconds() / 60  # minutes
        
        hint_views = len([s for s in steps if s['action_type'] == 'view_hint'])
        code_modifications = len([s for s in steps if s['action_type'] == 'modify_code'])
        tests_run = len([s for s in steps if s['action_type'] == 'test'])
        
        return {
            'attempt_id': attempt_id,
            'duration_minutes': round(duration, 2),
            'total_steps': len(steps),
            'hints_viewed': hint_views,
            'code_modifications': code_modifications,
            'tests_run': tests_run,
            'tests_passed': attempt['tests_passed'],
            'tests_total': attempt['tests_total'],
            'is_solved': bool(attempt['is_solved']),
            'success_rate': round(attempt['tests_passed'] / attempt['tests_total'] * 100, 1) if attempt['tests_total'] > 0 else 0
        }
