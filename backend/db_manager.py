"""
Database Manager
Quản lý lưu trữ users, code submissions và AI analysis
"""
import json
import sqlite3
import secrets
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash


class DatabaseManager:
    """Quản lý database SQLite"""
    
    def __init__(self, db_path="analyzer.db"):
        self.db_path = Path(db_path)
        self.init_database()
    
    def init_database(self):
        """Khởi tạo database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        obsolete_tables = ['problems', 'test_cases', 'hints', 'attempts', 'attempt_steps']
        for table_name in obsolete_tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                metadata TEXT,
                last_login TIMESTAMP,
                is_active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Ensure additional columns exist for older DBs: add if missing
        cursor.execute("PRAGMA table_info(users)")
        existing_cols = [row[1] for row in cursor.fetchall()]
        additional_columns = {
            'full_name': 'TEXT',
            'metadata': 'TEXT',
            'last_login': 'TIMESTAMP',
            'is_active': 'INTEGER DEFAULT 1'
        }
        for col, col_type in additional_columns.items():
            if col not in existing_cols:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col} {col_type}")
        
        # Create code submissions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS code_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                problem_id TEXT,
                code TEXT NOT NULL,
                compile_status TEXT,
                test_results TEXT,
                run_output TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create ai analysis table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submission_id INTEGER,
                classification TEXT,
                ai_analysis TEXT,
                sanitized_analysis TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (submission_id) REFERENCES code_submissions(id)
            )
        """)
        
        conn.commit()
        conn.close()

    # ============ CODE SUBMISSIONS / AI ANALYSIS ============

    def save_submission(self, user_id: int, problem_id: str, code: str, compile_status: dict = None, test_results: list = None, run_output: str = '') -> int:
        """Lưu một submission code (code submission)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO code_submissions (user_id, problem_id, code, compile_status, test_results, run_output)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            problem_id,
            code,
            json.dumps(compile_status) if compile_status is not None else None,
            json.dumps(test_results) if test_results is not None else None,
            run_output
        ))

        submission_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return submission_id

    def save_ai_analysis(self, submission_id: int, classification: dict, ai_analysis_text: str, sanitized_text: str = None) -> int:
        """Lưu kết quả phân tích AI liên quan đến một submission"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ai_analysis (submission_id, classification, ai_analysis, sanitized_analysis)
            VALUES (?, ?, ?, ?)
        """, (
            submission_id,
            json.dumps(classification) if classification is not None else None,
            ai_analysis_text,
            sanitized_text
        ))

        aid = cursor.lastrowid
        conn.commit()
        conn.close()
        return aid

    def get_submissions_by_user(self, user_id: int) -> list:
        """Lấy các code submissions của 1 user"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM code_submissions WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        conn.close()

        return [dict(r) for r in rows]
    
    # ============ USER MANAGEMENT ============
    
    def register_user(self, username: str, email: str, password: str, full_name: str = '', metadata: str = '') -> dict:
        """Đăng ký user mới"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = generate_password_hash(password)
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (username, email, password_hash, full_name, metadata))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'user_id': user_id,
                'username': username,
                'email': email,
                'full_name': full_name,
                'message': 'Đăng ký thành công'
            }
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return {'success': False, 'error': 'Username đã tồn tại'}
            elif 'email' in str(e):
                return {'success': False, 'error': 'Email đã tồn tại'}
            else:
                return {'success': False, 'error': str(e)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_by_username(self, username: str) -> dict:
        """Lấy thông tin user bằng username"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_user_by_id(self, user_id: int) -> dict:
        """Lấy thông tin user bằng ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, full_name, metadata, last_login, is_active, created_at FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def verify_password(self, username: str, password: str) -> dict:
        """Xác minh password của user"""
        user = self.get_user_by_username(username)
        
        if not user:
            return {'success': False, 'error': 'Username không tồn tại'}
        
        if check_password_hash(user['password_hash'], password):
            return {
                'success': True,
                'user_id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        else:
            return {'success': False, 'error': 'Password không chính xác'}

    def get_user_by_email(self, email: str) -> dict:
        """Lấy thông tin user bằng email"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None

    def get_or_create_google_user(self, email: str, full_name: str = '') -> dict:
        """Tìm hoặc tạo user từ Google OAuth
        
        Args:
            email: Email từ Google
            full_name: Tên đầy đủ từ Google
        
        Returns: 
            {
                'success': bool,
                'user_id': id của user,
                'username': username,
                'email': email,
                'is_new': True nếu vừa tạo, False nếu tìm thấy
            }
        """
        try:
            # Tìm user có email này
            user = self.get_user_by_email(email)
            
            if user:
                # User đã tồn tại
                return {
                    'success': True,
                    'user_id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'is_new': False
                }
            
            # Tạo user mới từ Google
            # Username: lấy từ email prefix (trước @)
            username_base = email.split('@')[0]
            username = username_base
            
            # Kiểm tra username đã tồn tại chưa
            counter = 1
            while self.get_user_by_username(username):
                username = f"{username_base}{counter}"
                counter += 1
            
            # Tạo password random (vì Google OAuth không cần password)
            random_password = secrets.token_urlsafe(16)
            
            # Lưu metadata rằng đây là Google user
            metadata = json.dumps({'auth_provider': 'google'})
            
            # Đăng ký user mới
            result = self.register_user(
                username=username,
                email=email,
                password=random_password,
                full_name=full_name,
                metadata=metadata
            )
            
            if result['success']:
                result['is_new'] = True
                return result
            else:
                return result
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
