"""
Database Models for Tracking Attempts
Lưu trữ vết tiến trình sửa lỗi
"""
from datetime import datetime


# SQLite Schema (có thể dùng SQLAlchemy)
DATABASE_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    c_code TEXT NOT NULL,
    bug_type TEXT NOT NULL,
    bug_taxonomy_id TEXT,
    expected_output TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS test_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id INTEGER NOT NULL,
    input TEXT,
    expected_output TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    problem_id INTEGER NOT NULL,
    
    -- Original code info
    original_code TEXT NOT NULL,
    bug_type TEXT,
    bug_taxonomy_id TEXT,
    
    -- Attempt tracking
    attempt_number INTEGER,
    current_code TEXT,
    
    -- Hints used
    hints_viewed TEXT,  -- JSON array of hint IDs
    current_hint_index INTEGER,
    
    -- Progress
    tests_passed INTEGER DEFAULT 0,
    tests_total INTEGER,
    is_solved BOOLEAN DEFAULT 0,
    
    -- Metadata
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_time TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);

CREATE TABLE IF NOT EXISTS attempt_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id INTEGER NOT NULL,
    
    -- Step details
    step_number INTEGER,
    action_type TEXT,  -- 'view_hint', 'modify_code', 'test', 'reset'
    
    -- Code state
    code_before TEXT,
    code_after TEXT,
    
    -- Hint info
    hint_id TEXT,
    hint_text TEXT,
    
    -- Test results
    test_results_json TEXT,  -- JSON of test results
    
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (attempt_id) REFERENCES attempts(id)
);

CREATE TABLE IF NOT EXISTS hints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id INTEGER NOT NULL,
    
    -- Hint content
    hint_level INTEGER,  -- 1=vague, 2=medium, 3=specific
    category TEXT,  -- 'logic', 'syntax', 'boundary', etc
    hint_text TEXT NOT NULL,
    
    -- Hint type
    hint_type TEXT,  -- 'question', 'tip', 'explanation', 'code_pattern'
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (problem_id) REFERENCES problems(id)
);
"""

# Python Classes for ORM (using simple dict-based for now)

class Attempt:
    """Represent một lần cố gắng sửa lỗi"""
    
    def __init__(self, user_id, problem_id, original_code, bug_type):
        self.id = None
        self.user_id = user_id
        self.problem_id = problem_id
        self.original_code = original_code
        self.bug_type = bug_type
        self.current_code = original_code
        self.attempt_number = 1
        self.hints_viewed = []
        self.current_hint_index = 0
        self.tests_passed = 0
        self.tests_total = 0
        self.is_solved = False
        self.steps = []
        self.start_time = datetime.now()
        self.last_modified = datetime.now()
        self.completed_time = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'problem_id': self.problem_id,
            'original_code': self.original_code,
            'current_code': self.current_code,
            'bug_type': self.bug_type,
            'attempt_number': self.attempt_number,
            'hints_viewed': self.hints_viewed,
            'current_hint_index': self.current_hint_index,
            'tests_passed': self.tests_passed,
            'tests_total': self.tests_total,
            'is_solved': self.is_solved,
            'step_count': len(self.steps),
            'start_time': self.start_time.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'completed_time': self.completed_time.isoformat() if self.completed_time else None
        }


class AttemptStep:
    """Represent một step trong attempt"""
    
    def __init__(self, step_number, action_type):
        self.id = None
        self.step_number = step_number
        self.action_type = action_type  # 'view_hint', 'modify_code', 'test', 'reset'
        self.code_before = None
        self.code_after = None
        self.hint_id = None
        self.hint_text = None
        self.test_results = {}
        self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'step_number': self.step_number,
            'action_type': self.action_type,
            'code_before': self.code_before,
            'code_after': self.code_after,
            'hint_id': self.hint_id,
            'test_results': self.test_results,
            'timestamp': self.timestamp.isoformat()
        }


class Hint:
    """Represent một gợi ý"""
    
    def __init__(self, problem_id, hint_level, category, hint_text, hint_type):
        self.id = None
        self.problem_id = problem_id
        self.hint_level = hint_level  # 1=vague, 2=medium, 3=specific
        self.category = category  # 'logic', 'syntax', 'boundary'
        self.hint_text = hint_text
        self.hint_type = hint_type  # 'question', 'tip', 'explanation', 'code_pattern'
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'problem_id': self.problem_id,
            'hint_level': self.hint_level,
            'category': self.category,
            'hint_text': self.hint_text,
            'hint_type': self.hint_type,
            'created_at': self.created_at.isoformat()
        }
