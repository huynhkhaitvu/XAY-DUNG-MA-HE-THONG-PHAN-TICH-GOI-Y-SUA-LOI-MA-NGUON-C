# 🎓 INTERACTIVE LEARNING SYSTEM - IDEA

**Ngày Tạo:** May 11, 2026  
**Phiên Bản:** 2.0 (Enhanced)  
**Loại:** System Architecture Upgrade

---

## 📝 TỔNG QUAN

Nâng cấp hệ thống từ "phân tích & gợi ý" sang **"học tập interactively với tracking"**:

**Cũ:** User nhập code → AI phân tích → Cung cấp gợi ý hoàn chỉnh  
**Mới:** User nhập code → AI phân tích → Gợi ý từng bước (Level 1→2→3) → Track progress

---

## 🎯 OBJECTIVE

Tạo một **học tập interactively** giúp người dùng:
1. **Tự phát hiện lỗi** thông qua hints hướng dẫn
2. **Học process** chứ không chỉ learn solution
3. **Track progress** qua attempt database
4. **Cải thiện kỹ năng** bằng feedback từng bước

---

## 🏗️ KIẾN TRÚC

### Đầu Vào (Input Layer)

```
1. File C đơn
2. Bug Taxonomy (Danh mục bugs)
   - CF001: Conditional Logic Error
   - CF002: Missing Branch
   - CF003: Nested Condition Error
   - CF004: Operator Precedence
   - CF005: Switch/Case Error
   - CF006: Boundary Condition Error
   - CF007: Type Comparison Error

3. Requirements (Yêu cầu đề bài)
4. Test Cases (Testcases)
```

### Processing Layer

```
┌─────────────────────────────────┐
│  Smart Prompt Generator         │
├─────────────────────────────────┤
│ - Analyze code structure        │
│ - Detect bug type               │
│ - Build context-aware prompts   │
└──────────┬──────────────────────┘
           │
           ↓
┌─────────────────────────────────┐
│  AI API (Gemini)                │
├─────────────────────────────────┤
│ - Analyze code & bugs           │
│ - Generate hints level-by-level │
│ - Create guidance               │
│ - Provide step-by-step path     │
└──────────┬──────────────────────┘
           │
           ↓
┌─────────────────────────────────┐
│  Hint Service                   │
├─────────────────────────────────┤
│ - Format hints                  │
│ - Cache results                 │
│ - Generate follow-up questions  │
└──────────┬──────────────────────┘
           │
           ↓
┌─────────────────────────────────┐
│  Test & Verification Engine     │
├─────────────────────────────────┤
│ - Compile C code (GCC)          │
│ - Run testcases                 │
│ - Compare output                │
│ - Track progress                │
└──────────┬──────────────────────┘
           │
           ↓
┌─────────────────────────────────┐
│  Database Manager               │
├─────────────────────────────────┤
│ - Save attempts                 │
│ - Track steps                   │
│ - Store progress                │
└─────────────────────────────────┘
```

### Đầu Ra (Output Layer)

```
1. Attempt Record
   - Original code
   - Bug type
   - All modifications
   - Hints viewed
   - Tests passed/failed
   - Time spent
   - Final solution

2. Progress Tracking
   - Step-by-step history
   - Hints used
   - Test results
   - Success rate
```

---

## 📊 BUG TAXONOMY (Miền Kiến Thức)

Tập trung vào **Cấu Trúc Rẽ Nhánh (Control Flow)**:

| Bug ID | Name | Description | Example |
|--------|------|-------------|---------|
| CF001 | Conditional Logic | Điều kiện sai | `if (x < 5)` vs `if (x <= 5)` |
| CF002 | Missing Branch | Thiếu case | Không xử lý `x == 0` |
| CF003 | Nested Condition | Lồng nhau sai | Else thuộc if nào? |
| CF004 | Operator Precedence | Thứ tự ưu tiên sai | `a && b \|\| c` |
| CF005 | Switch/Case | Fall-through hoặc thiếu break | Quên break; |
| CF006 | Boundary | Off-by-one error | `i < n` vs `i <= n` |
| CF007 | Type Comparison | So sánh kiểu sai | `char '5'` vs `int 5` |

---

## 🎓 LEARNING FLOW

### Step 1: Start Session
```
User → Nhập code, requirements, testcases
     → Chọn bug type (từ taxonomy)
     → System khởi tạo attempt
```

### Step 2: Initial Analysis
```
System → Gọi AI với smart prompt
      → AI phân tích code
      → Trả về: branch info, root cause, guided questions
      → Hiển thị trên UI
```

### Step 3: Hint Progression (Level 1→2→3)

**Level 1 - Vague (Mơ hồ):**
```
"Kiểm tra lại điều kiện trong if"
"Vẽ sơ đồ: input nào → output nào"
```

**Level 2 - Medium (Trung bình):**
```
"So sánh output thực tế vs expected"
"Test case nào sai?"
"Toán tử so sánh có đúng không?"
```

**Level 3 - Specific (Cụ thể):**
```
"Điều kiện nên là x <= 5 chứ không phải x < 5"
"Lý do: requirement yêu cầu bao gồm x = 5"
"Hãy thử sửa dòng này"
```

### Step 4: User Modifies Code
```
User → Chỉnh sửa code
    → Nhấp "Run Test"
    → System chạy testcases
    → Hiển thị kết quả
```

### Step 5: Progress Tracking
```
System → Lưu mỗi bước (step)
      → Track: code change, hints used, test results
      → Update progress bar
      → Provide next guidance
```

### Step 6: Completion
```
When all tests pass:
- Mark as solved
- Save attempt with metadata
- Show statistics
- Celebrate!
```

---

## 💾 DATABASE SCHEMA

### Table: `attempts`
```
id              INTEGER PK
user_id         TEXT
problem_id      TEXT
original_code   TEXT
bug_type        TEXT
current_code    TEXT
attempt_number  INTEGER
hints_viewed    JSON (array of hint IDs)
tests_passed    INTEGER
tests_total     INTEGER
is_solved       BOOLEAN
start_time      TIMESTAMP
last_modified   TIMESTAMP
completed_time  TIMESTAMP
```

### Table: `attempt_steps`
```
id              INTEGER PK
attempt_id      INTEGER FK
step_number     INTEGER
action_type     TEXT (view_hint, modify_code, test, reset)
code_before     TEXT
code_after      TEXT
hint_id         TEXT
hint_text       TEXT
test_results    JSON
timestamp       TIMESTAMP
```

**Ví dụ Attempt:**
```
Attempt #1:
- User: john123
- Problem: Fix conditional logic
- Original: if (x < 5) printf("Less");
- Status: SOLVED
- Steps:
  1. View hint level 1
  2. Modify code to: if (x <= 5)
  3. Run test → 2/3 passed
  4. View hint level 2
  5. Modify code (adjust comparison)
  6. Run test → 3/3 passed ✓
- Time: 12 minutes
- Hints used: 2
- Success rate: 100%
```

---

## 🔌 API ENDPOINTS

### Interactive Learning Endpoints

```
POST /api/interactive/start-learning
  Input: code, requirements, testcases, bug_taxonomy_id
  Output: attempt_id, analysis, initial_hints

POST /api/interactive/get-hint
  Input: attempt_id, hint_level, test_case, error_info
  Output: hint_text, follow_up_question, code_area

POST /api/interactive/modify-code
  Input: attempt_id, new_code, testcases
  Output: test_results, is_solved, progress

POST /api/interactive/get-guidance
  Input: attempt_id, requirements, testcases
  Output: current_issues, next_step

GET /api/interactive/get-attempt/<attempt_id>
  Output: attempt_data, steps, statistics

GET /api/interactive/get-user-attempts/<user_id>
  Output: list of attempts with stats

GET /api/interactive/get-bug-taxonomy
  Output: bug_taxonomy catalog
```

---

## 🎨 USER INTERFACE

### Layout (2-Panel)

**Left Panel: Code Editor**
- Syntax highlighting
- Line numbers
- Current code display

**Right Panel: Hints & Guidance**
- Initial analysis
- Hint buttons (Level 1, 2, 3)
- Test results display
- Progress tracker
- History

---

## 🧠 SMART PROMPT GENERATION

### Template 1: Analysis Prompt
```python
# Input: code, bug_type, requirements, testcases
# Output: branches analysis, root cause, guided questions, hints

prompt = """
You are a C programming teacher.
Task: Analyze code and find logical errors.

CODE:
```c
[code]
```

REQUIREMENTS:
[requirements]

TEST CASES:
[testcases]

ANALYZE:
1. Count branches in code
2. Check each condition
3. Compare with requirements
4. Identify wrong conditions

RETURN JSON:
{
  "branches": [...],
  "root_cause": "...",
  "guided_questions": [...],
  "hints": [
    {"level": 1, "hint": "..."},
    {"level": 2, "hint": "..."},
    {"level": 3, "hint": "..."}
  ]
}
"""
```

### Template 2: Hint Progression Prompt
```python
# Input: code, bug_type, current_hint_level, test_case, error_info
# Output: hint at specific level

# Level 1: Very vague question
"Have you checked the condition in this if statement?"

# Level 2: Medium hint
"Look at test case 2: when input=5, what should output be?
Your code outputs X, but expected Y. Which operator is wrong?"

# Level 3: Specific hint
"The condition should be `x <= 5` not `x < 5`.
The requirement says '5 should be included'."
```

---

## 📈 TRACKING & ANALYTICS

### Per-Attempt Stats
- ⏱️ Duration: 12 minutes
- 📊 Steps: 6 total
- 💡 Hints: Viewed 2 (Level 1, 2)
- ✏️ Modifications: 3 code changes
- 🧪 Tests: 3 total, 3 passed
- ✅ Success: Yes (100%)

### User Progress
- Total attempts: 5
- Solved: 4
- Average time: 10.5 minutes
- Most used hint level: Level 2
- Improvement: Getting faster

---

## 🔄 ITERATIVE WORKFLOW

```
Session Start
     ↓
[Analysis Phase]
Display: branches, root_cause, questions
     ↓
[Hint Phase - Loop]
User views hint (L1→L2→L3)
     ↓
[Modification Phase]
User edits code
     ↓
[Test Phase]
Run testcases
     ↓
All pass? → YES → [Completion]
         ↘
           NO → Repeat hint/modify phase
               ↑
           (Track each step)
```

---

## 🎁 BENEFITS

### For Learners
✅ Learn thinking process, not just solution  
✅ Progressive hints prevent frustration  
✅ Immediate feedback  
✅ Can see their own progress  
✅ Reusable for future problems  

### For Instructors
✅ Track student progress  
✅ Identify common misconceptions  
✅ Understand learning patterns  
✅ Provide targeted feedback  

### For System
✅ Data on what hints work  
✅ Improve prompt generation  
✅ AI learns from attempt patterns  

---

## 🚀 TECHNICAL STACK

- **Backend:** Flask + SQLite
- **Database:** SQLite (attempts, steps, hints)
- **AI:** Gemini API (smart prompting)
- **Compilation:** GCC
- **Frontend:** HTML5 + Bootstrap + Vanilla JS
- **API Style:** RESTful JSON

---

## 📋 FILES CREATED

**Backend:**
- `bug_taxonomy.py` - Bug classification system
- `models.py` - Attempt, Step, Hint data models
- `prompt_generator.py` - Smart prompt creation
- `hint_service.py` - Hint generation & caching
- `db_manager.py` - SQLite database management
- `learning_routes.py` - Flask routes for interactive mode

**Frontend:**
- `learning.html` - Interactive UI
- `learning.js` - Client-side logic

---

## 🎯 FUTURE ENHANCEMENTS

1. **Multiple Knowledge Domains:**
   - Loops (CF_LOOPS)
   - Arrays (CF_ARRAYS)
   - Functions (CF_FUNCTIONS)
   - Pointers (CF_POINTERS)

2. **Advanced Analytics:**
   - Learning curve tracking
   - Recommendation system
   - Personalized hints

3. **Collaborative Features:**
   - Share sessions
   - Peer code review
   - Discussion board

4. **Gamification:**
   - Points & badges
   - Leaderboard
   - Achievements

5. **AI Improvements:**
   - Fine-tuned models
   - Hint quality scoring
   - Adaptive difficulty

---

## 📊 EXPECTED OUTCOMES

**Before:** User gets stuck → views full solution → doesn't learn  
**After:** User gets stuck → views progressive hints → solves themselves → learns better

**Measurable:**
- ↑ Learning retention
- ↓ Time to solution
- ↓ Help desk tickets
- ↑ Student satisfaction

---

## ✅ IMPLEMENTATION STATUS

| Component | Status | Lines |
|-----------|--------|-------|
| Bug Taxonomy | ✅ Done | 150+ |
| Models | ✅ Done | 180+ |
| Prompt Generator | ✅ Done | 200+ |
| Hint Service | ✅ Done | 180+ |
| DB Manager | ✅ Done | 250+ |
| Learning Routes | ✅ Done | 350+ |
| Frontend HTML | ✅ Done | 200+ |
| Frontend JS | ✅ Done | 300+ |
| **Total** | ✅ **Done** | **~2000+** |

---

**Status:** 🎉 **READY FOR TESTING**

Next: Integration testing, UI refinement, documentation

---

**Created by:** GitHub Copilot  
**Date:** May 11, 2026
