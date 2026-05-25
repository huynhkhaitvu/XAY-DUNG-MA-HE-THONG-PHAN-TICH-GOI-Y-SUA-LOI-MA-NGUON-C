// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    renderTestCases();
    checkBackendConnection();
});

// Check backend connection
async function checkBackendConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend connected');
        }
    } catch (error) {
        console.warn('⚠️ Backend not available yet. Start backend with: python app.py');
    }
}

// Event Listeners
function initializeEventListeners() {
    document.getElementById('compileBtn').addEventListener('click', handleCompile);
    document.getElementById('runBtn').addEventListener('click', handleRun);
    document.getElementById('analyzeBtn').addEventListener('click', handleAnalyze);
    document.getElementById('executeBtn').addEventListener('click', handleExecute);
    document.getElementById('clearBtn').addEventListener('click', handleClear);
    document.getElementById('addTestCaseBtn').addEventListener('click', handleAddTestCase);
}

// Get code
function getCode() {
    return document.getElementById('codeEditor').value;
}

// Get test cases
function getTestCases() {
    const testCases = [];
    const testElements = document.querySelectorAll('.test-case');
    testElements.forEach(el => {
        const input = el.querySelector('.test-input').value;
        const output = el.querySelector('.test-output').value;
        if (input || output) {
            testCases.push({
                input: input,
                expected_output: output
            });
        }
    });
    return testCases;
}

// Handle Compile
async function handleCompile() {
    const code = getCode();
    if (!code.trim()) {
        showError('Vui lòng nhập mã C');
        return;
    }

    showLoading('compileSpinner');
    try {
        const response = await fetch(`${API_BASE_URL}/compile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code })
        });

        const data = await response.json();
        hideLoading('compileSpinner');

        if (data.success) {
            showSuccess('✓ Biên dịch thành công');
        } else {
            showError(data.error || 'Biên dịch thất bại');
        }
    } catch (error) {
        hideLoading('compileSpinner');
        showError('Lỗi kết nối: ' + error.message);
    }
}

// Handle Run (in modal)
async function handleRun() {
    const code = getCode();
    if (!code.trim()) {
        showError('Vui lòng nhập mã C');
        return;
    }
}

// Handle Execute
async function handleExecute() {
    const code = getCode();
    const input = document.getElementById('programInput').value;

    if (!code.trim()) {
        showError('Vui lòng nhập mã C');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, input })
        });

        const data = await response.json();

        let resultHTML = '<div class="alert alert-info alert-custom"><strong>Output:</strong></div>';
        resultHTML += `<pre>${escapeHtml(data.output || data.error)}</pre>`;

        if (data.error && data.error.trim()) {
            resultHTML = '<div class="alert alert-error alert-custom"><strong>Lỗi Runtime:</strong></div>';
            resultHTML += `<pre>${escapeHtml(data.error)}</pre>`;
        }

        document.getElementById('resultsContainer').innerHTML = resultHTML;
        bootstrap.Modal.getInstance(document.getElementById('runModal')).hide();

    } catch (error) {
        showError('Lỗi kết nối: ' + error.message);
    }
}

// Handle Analyze
async function handleAnalyze() {
    const code = getCode();
    const testcases = getTestCases();

    if (!code.trim()) {
        showError('Vui lòng nhập mã C');
        return;
    }

    showLoading('analyzeSpinner');
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, testcases })
        });

        const data = await response.json();
        hideLoading('analyzeSpinner');

        let resultHTML = '';

        // Compile status
        if (data.compile_status) {
            if (data.compile_status.success) {
                resultHTML += '<div class="alert alert-success alert-custom">✓ Biên dịch thành công</div>';
            } else {
                resultHTML += '<div class="alert alert-error alert-custom">';
                resultHTML += '<strong>Lỗi biên dịch:</strong>';
                resultHTML += `<div class="error-details">${escapeHtml(data.compile_status.error)}</div>`;
                resultHTML += '</div>';
            }
        }

        // Test results
        if (data.test_results && data.test_results.length > 0) {
            resultHTML += '<h6 class="mt-3">Test Results:</h6>';
            data.test_results.forEach((test, idx) => {
                const status = test.passed ? '✓ PASS' : '✗ FAIL';
                const statusClass = test.passed ? 'passed' : 'failed';
                resultHTML += `<div class="test-case-result ${statusClass}">`;
                resultHTML += `<strong>Test ${idx + 1}: ${status}</strong><br>`;
                resultHTML += `Input: ${escapeHtml(test.input)}<br>`;
                resultHTML += `Expected: ${escapeHtml(test.expected)}<br>`;
                resultHTML += `Actual: ${escapeHtml(test.actual)}`;
                resultHTML += '</div>';
            });
        }

        // AI Suggestions
        if (data.ai_suggestions) {
            resultHTML += '<div class="suggestion-box mt-3">';
            resultHTML += '<h6>💡 Gợi ý từ AI:</h6>';
            resultHTML += `<div class="suggestion-text">${data.ai_suggestions}</div>`;
            resultHTML += '</div>';
        }

        // Errors
        if (data.errors && data.errors.length > 0) {
            resultHTML += '<div class="alert alert-error alert-custom mt-3">';
            resultHTML += '<strong>Lỗi:</strong><ul>';
            data.errors.forEach(err => {
                resultHTML += `<li>${escapeHtml(err)}</li>`;
            });
            resultHTML += '</ul></div>';
        }

        if (!resultHTML.trim()) {
            resultHTML = '<p class="text-muted">Không có kết quả</p>';
        }

        document.getElementById('resultsContainer').innerHTML = resultHTML;

    } catch (error) {
        hideLoading('analyzeSpinner');
        showError('Lỗi kết nối: ' + error.message);
    }
}

// Handle Add Test Case
function handleAddTestCase() {
    const container = document.getElementById('testCasesContainer');
    const count = container.children.length + 1;

    const html = `
        <div class="test-case">
            <div class="row">
                <div class="col-md-6">
                    <label class="form-label">Input:</label>
                    <textarea class="form-control test-input" style="height: 60px;" placeholder="Input"></textarea>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Expected Output:</label>
                    <textarea class="form-control test-output" style="height: 60px;" placeholder="Expected Output"></textarea>
                </div>
            </div>
            <button class="btn btn-outline-danger btn-sm mt-2" onclick="this.parentElement.remove();">✕ Xóa</button>
        </div>
    `;

    container.insertAdjacentHTML('beforeend', html);
}

// Handle Clear
function handleClear() {
    if (confirm('Bạn có chắc chắn muốn xóa mã?')) {
        document.getElementById('codeEditor').value = '';
        document.getElementById('resultsContainer').innerHTML = '<p class="text-muted">Kết quả sẽ hiển thị tại đây...</p>';
    }
}

// Render test cases
function renderTestCases() {
    // Mặc định có 1 test case trống
    handleAddTestCase();
}

// Show/Hide Loading
function showLoading(id) {
    document.getElementById(id).classList.remove('d-none');
}

function hideLoading(id) {
    document.getElementById(id).classList.add('d-none');
}

// Show Messages
function showSuccess(message) {
    const html = `<div class="alert alert-success alert-custom">${message}</div>`;
    document.getElementById('resultsContainer').innerHTML = html + document.getElementById('resultsContainer').innerHTML;
}

function showError(message) {
    const html = `<div class="alert alert-error alert-custom"><strong>Lỗi:</strong> ${escapeHtml(message)}</div>`;
    document.getElementById('resultsContainer').innerHTML = html + document.getElementById('resultsContainer').innerHTML;
}

// Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
