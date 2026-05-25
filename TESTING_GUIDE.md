# 🧪 TESTING GUIDE - Interactive Learning System

**Status:** Ready for Testing  
**Date:** May 11, 2026

---

## 📋 Prerequisites

### 1. Environment Setup

```bash
# 1. Verify Python
python --version  # Should be 3.12.6+

# 2. Navigate to backend
cd backend

# 3. Create/activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# 4. Install dependencies
pip install -r requirements.txt

# 5. Check .env file
cat .env  # Should contain GEMINI_API_KEY
```

### 2. GCC Installation (Windows)

**STATUS:** ⏳ Still needed

```bash
# Option 1: Using MinGW-W64 installer
1. Download: https://www.mingw-w64.org/downloads/
2. Run installer
3. Select: x86_64 architecture
4. Install to: C:\Program Files\mingw-w64\
5. Add to PATH: C:\Program Files\mingw-w64\bin
6. Verify: gcc --version

# Option 2: Using Chocolatey (if installed)
choco install mingw

# Verify installation
gcc --version
```

---

## 🧪 Test Suite

### Phase 1: Database Initialization ✅

```bash
# Test 1.1: Initialize database
python -c "
from db_manager import DatabaseManager
db = DatabaseManager()
print('✓ Database initialized successfully')
print('✓ Tables created')
"

# Test 1.2: Create a test attempt
python -c "
from db_manager import DatabaseManager
from models import Attempt
db = DatabaseManager()
attempt = Attempt(
    user_id='test_user',
    problem_id='test_prob',
    original_code='int main() {}',
    bug_type='TEST'
)
attempt_id = db.save_attempt(attempt)
print(f'✓ Attempt created: ID={attempt_id}')
"
```

**Expected Output:**
```
✓ Database initialized successfully
✓ Tables created
✓ Attempt created: ID=1
```

---

### Phase 2: Code Analysis & Compilation ✅

```bash
# Test 2.1: Analyze sample code
python -c "
from analyzer import CodeAnalyzer
analyzer = CodeAnalyzer()

code = '''
#include <stdio.h>
int main() {
    int x = 5;
    if (x < 5) {
        printf(\"Less than 5\");
    }
    return 0;
}
'''

result = analyzer.analyze(code, [])
print(f'Analysis: {result}')
"

# Test 2.2: Compile and run code
python -c "
from analyzer import CodeAnalyzer
analyzer = CodeAnalyzer()

code = '''
#include <stdio.h>
int main() {
    printf(\"Hello\");
    return 0;
}
'''

result = analyzer.run(code, '')
print(f'Output: {result}')
"
```

**Expected Output:**
```
Output: {'success': True, 'output': 'Hello', 'error': ''}
```

---

### Phase 3: Hint Generation 🧪

```bash
# Test 3.1: Generate hints
python -c "
from hint_service import HintService
from ai_handler import AIHandler

ai = AIHandler()
hint_service = HintService(ai)

analysis = hint_service.analyze_and_create_hints(
    code='if (x < 5) printf(\"less\");',
    bug_type='CONDITIONAL_LOGIC',
    bug_taxonomy_id='CF001',
    requirements='Check if x is less than or equal to 5',
    test_cases=[{'input': '5', 'expected_output': 'less'}]
)

print('Analysis result:')
print(analysis)
"
```

**Expected Output:**
```
Analysis result:
{
    'bugs_detected': [...],
    'hints': [
        {'level': 1, 'hint': 'Check the condition...'},
        {'level': 2, 'hint': 'Compare with test case...'},
        {'level': 3, 'hint': 'Change < to <=...'}
    ]
}
```

---

### Phase 4: API Endpoints 🧪

#### Start Learning Session

```bash
# Test 4.1: POST /api/interactive/start-learning
curl -X POST http://localhost:5000/api/interactive/start-learning \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "problem_id": "loop_error_1",
    "code": "#include <stdio.h>\nint main() { for(int i=0; i<5; i++) printf(\"%d \", i); }",
    "requirements": "Print 0 1 2 3 4",
    "testcases": [{"input": "", "expected_output": "0 1 2 3 4"}],
    "bug_type": "LOOP_ERROR",
    "bug_taxonomy_id": "LP001"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "attempt_id": 1,
  "analysis": { ... },
  "initial_hints": [ ... ]
}
```

#### Get Hints

```bash
# Test 4.2: POST /api/interactive/get-hint
curl -X POST http://localhost:5000/api/interactive/get-hint \
  -H "Content-Type: application/json" \
  -d '{
    "attempt_id": 1,
    "hint_level": 1,
    "bug_taxonomy_id": "LP001"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "hint": {
    "level": 1,
    "hint_text": "Check your loop condition...",
    "follow_up": "What should the loop do for index 5?"
  },
  "step_number": 2
}
```

#### Modify Code

```bash
# Test 4.3: POST /api/interactive/modify-code
curl -X POST http://localhost:5000/api/interactive/modify-code \
  -H "Content-Type: application/json" \
  -d '{
    "attempt_id": 1,
    "new_code": "#include <stdio.h>\nint main() { for(int i=0; i<=5; i++) printf(\"%d \", i); }",
    "testcases": [{"input": "", "expected_output": "0 1 2 3 4"}]
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "test_results": [
    {
      "testcase": 1,
      "passed": false,
      "input": "",
      "expected": "0 1 2 3 4",
      "actual": "0 1 2 3 4 5"
    }
  ],
  "passed": 0,
  "total": 1,
  "is_solved": false,
  "step_number": 3
}
```

---

### Phase 5: Full Workflow Test 🎯

**Scenario:** Fix a conditional logic error

1. **Start session:**
```bash
POST /api/interactive/start-learning
Input: Loop error code + test cases
Output: attempt_id=1, bugs_detected=[...]
```

2. **View hints:**
```bash
POST /api/interactive/get-hint
Input: attempt_id=1, hint_level=1
Output: "Check if your condition includes the boundary value"
```

3. **Modify code:**
```bash
POST /api/interactive/modify-code
Input: attempt_id=1, new_code="..."
Output: Tests passed/failed, progress
```

4. **Check final state:**
```bash
GET /api/interactive/get-attempt/1
Output: Full history with all steps
```

---

## 🔧 Troubleshooting

### Error: "Module not found: analyzer"

**Solution:** Make sure you're in `backend/` directory
```bash
cd backend
python app.py
```

### Error: "GCC not found"

**Solution:** Install MinGW-W64 and add to PATH
```bash
gcc --version
# If not found, install from https://www.mingw-w64.org/
```

### Error: "Database locked"

**Solution:** Only one process can access SQLite at a time
```bash
# Close other Python processes
# Restart the server
```

### Error: "GEMINI_API_KEY not found"

**Solution:** Check .env file
```bash
cat .env
# Should contain: GEMINI_API_KEY=AIzaSy...
```

---

## 📊 Test Results Template

Use this template to document test results:

```markdown
### Test: [Name]
- **Status:** PASS / FAIL
- **Input:** [...]
- **Expected:** [...]
- **Actual:** [...]
- **Error:** [if any]
- **Notes:** [additional info]
```

---

## 🚀 Running Full System

### Terminal 1: Start Backend
```bash
cd backend
.\venv\Scripts\Activate.ps1
python app.py
# Server running at http://localhost:5000
```

### Terminal 2: Start Frontend
```bash
# Open in browser
file:///path/to/frontend/learning.html
# Or use simple server
cd frontend
python -m http.server 8000
# Visit http://localhost:8000/learning.html
```

### Terminal 3: Test with cURL
```bash
# Test endpoints (see Phase 4 above)
curl http://localhost:5000/api/health
```

---

## ✅ Checklist

- [ ] Python environment configured
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] GCC installed and in PATH
- [ ] Database initializes without errors
- [ ] Analyzer can compile C code
- [ ] Hint service generates hints
- [ ] All API endpoints respond correctly
- [ ] Frontend loads learning.html
- [ ] Full workflow completes successfully
- [ ] Database records attempts correctly

---

## 📈 Performance Benchmarks

Expected performance targets:

| Operation | Expected Time |
|-----------|---------------|
| Database init | < 100ms |
| Compile code | < 500ms |
| Generate hints | < 2000ms (API call) |
| Save attempt | < 50ms |
| Get user attempts | < 100ms |

---

## 🎓 Sample Test Data

### Sample 1: Loop Error
```c
#include <stdio.h>
int main() {
    for (int i = 0; i < 5; i++) {
        printf("%d ", i);
    }
    return 0;
}
```
- Bug: Off-by-one (should be i <= 5 if including 5)
- Expected: "0 1 2 3 4"
- Bug ID: LP001

### Sample 2: Conditional Logic Error
```c
#include <stdio.h>
int main() {
    int x = 5;
    if (x < 5) {
        printf("Less");
    } else {
        printf("Greater or equal");
    }
    return 0;
}
```
- Bug: Wrong operator (should be x <= 5)
- Expected: "Greater or equal" (for x=5)
- Bug ID: CF001

---

**Status:** Ready for integration testing  
**Next:** Execute test suite and fix any issues

---

*Last Updated: May 11, 2026*
*For issues: Check IDEA_INTERACTIVE_LEARNING.md*
