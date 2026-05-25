# 👨‍💻 DEVELOPER GUIDE

Hướng dẫn phát triển thêm tính năng cho C Code Analyzer.

## 🏗️ Project Structure

```
backend/
├── app.py              # Flask app chính - Entry point
├── analyzer.py         # Logic phân tích & biên dịch C
├── ai_handler.py       # Xử lý API Gemini
├── config.py           # Configuration
├── utils.py            # Utility functions
├── test_setup.py       # Setup testing
└── venv/               # Virtual environment

frontend/
├── index.html          # Giao diện chính
├── style.css           # Styling
└── script.js           # Client-side logic
```

## 🔧 Development Setup

```bash
# Clone repo
git clone <repo-url>
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac: source venv/bin/activate

# Install dev dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
pytest

# Format code
black *.py

# Lint
flake8 *.py
```

## 📝 Code Style

### Python
- PEP 8 style guide
- Type hints where possible
- Docstrings for functions
- Max 88 chars per line (Black)

Example:
```python
def analyze_code(code: str, testcases: list = None) -> dict:
    """
    Analyze C code and return results.
    
    Args:
        code: C source code
        testcases: List of test case dicts
        
    Returns:
        Analysis result dictionary
    """
    result = {}
    # ... implementation
    return result
```

### JavaScript
- Camel case for functions/variables
- Use async/await instead of promises
- Add comments for complex logic
- ESLint compliant

Example:
```javascript
async function analyzeCode() {
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Analysis failed:', error);
    }
}
```

## 🧪 Testing

### Run Tests
```bash
cd backend
pytest test_*.py -v
```

### Write Test
```python
# test_analyzer.py
import pytest
from analyzer import CodeAnalyzer

def test_compile_simple_code():
    analyzer = CodeAnalyzer()
    code = '#include <stdio.h>\nint main() { return 0; }'
    result = analyzer.compile(code)
    assert result['success'] == True
```

### Test Coverage
```bash
pytest --cov=. --cov-report=html
```

## 🚀 Adding New Features

### Feature: Add new AI provider (e.g., ChatGPT)

1. **Create new AI handler**
```python
# ai_handler.py - Add class
class ChatGPTHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.openai.com/v1'
    
    def get_suggestions(self, code):
        # Implementation
        pass
```

2. **Update app.py**
```python
from ai_handler import ChatGPTHandler

if provider == 'chatgpt':
    ai_handler = ChatGPTHandler(api_key)
```

3. **Test thoroughly**
```bash
pytest test_ai.py -v
```

### Feature: Add code formatting

1. **Add to utils.py**
```python
def format_c_code(code):
    """Format C code with proper indentation"""
    # Implementation using indent library or manual logic
    pass
```

2. **Add API endpoint**
```python
@app.route('/api/format', methods=['POST'])
def format_code():
    code = request.json.get('code')
    formatted = format_c_code(code)
    return {'formatted': formatted}
```

3. **Add frontend button**
```html
<button id="formatBtn">Format Code</button>
```

4. **Add JavaScript handler**
```javascript
document.getElementById('formatBtn').addEventListener('click', async () => {
    const code = getCode();
    const response = await fetch(`${API_BASE_URL}/format`, {
        method: 'POST',
        body: JSON.stringify({code})
    });
    const data = await response.json();
    document.getElementById('codeEditor').value = data.formatted;
});
```

## 🐛 Debugging

### Backend Debugging
```python
# Use Flask debugger
app.run(debug=True)

# Or use Python debugger
import pdb
pdb.set_trace()  # Set breakpoint
```

### Frontend Debugging
- Open DevTools: F12
- Set breakpoints in Sources tab
- Check Console for errors
- Monitor Network tab for API calls

### GCC Debugging
```python
# Print compile output
result = subprocess.run(
    ['gcc', c_file, '-o', exe_file],
    capture_output=True,
    text=True
)
print(result.stdout)
print(result.stderr)
```

## 📚 API Documentation

### Add New Endpoint

1. **Implement handler**
```python
@app.route('/api/new-feature', methods=['POST'])
def new_feature():
    """
    Description of endpoint
    
    Request JSON:
    {
        "param1": "value1"
    }
    
    Response:
    {
        "result": "value"
    }
    """
    try:
        data = request.get_json()
        # Implementation
        return jsonify({'result': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

2. **Document in README**
```markdown
### POST /api/new-feature
Description...

Request:
```json
{...}
```

Response:
```json
{...}
```
```

## 🔍 Common Issues & Solutions

### Issue: GCC not found in subprocess
**Solution:** Use full path or update PATH
```python
gcc_path = 'C:\\mingw64\\bin\\gcc.exe'
subprocess.run([gcc_path, ...])
```

### Issue: CORS error when testing
**Solution:** Ensure CORS is enabled
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Issue: API timeout
**Solution:** Add timeout parameter
```python
response = requests.post(url, timeout=30)
```

### Issue: Frontend not connecting to backend
**Solution:** Check API_BASE_URL in script.js
```javascript
const API_BASE_URL = 'http://localhost:5000/api';  // Verify port
```

## 📖 Resources

- Flask docs: https://flask.palletsprojects.com/
- Python requests: https://requests.readthedocs.io/
- Gemini API: https://ai.google.dev/
- Bootstrap: https://getbootstrap.com/docs/5.3/

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes
3. Test thoroughly: `pytest`
4. Commit: `git commit -am 'Add new feature'`
5. Push: `git push origin feature/new-feature`
6. Create Pull Request

---

**Happy coding! 🎉**
