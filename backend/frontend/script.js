// API Configuration: use relative path so requests are same-origin
const API_BASE_URL = '/api';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    checkUserAuthAndRedirect();
    initializeEventListeners();
    renderTestCases();
    checkBackendConnection();
    checkUserAuth();
    setupLogout();
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
    document.getElementById('analyzeBtn').addEventListener('click', openRequirementsModal);
    const requirementsAnalyzeBtn = document.getElementById('requirementsAnalyzeBtn');
    if (requirementsAnalyzeBtn) {
        requirementsAnalyzeBtn.addEventListener('click', handleRequirementsAnalyze);
    }
    document.getElementById('clearBtn').addEventListener('click', handleClear);
    document.getElementById('addTestCaseBtn').addEventListener('click', handleAddTestCase);
    // File open button handlers
    const openBtn = document.getElementById('openFileBtn');
    const fileInput = document.getElementById('fileInput');
    if (openBtn && fileInput) {
        openBtn.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', handleFileSelect);
    }
}

// Handle file selection: read first file and put into editor
function handleFileSelect(event) {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];
    const maxSize = 1024 * 1024; // 1MB limit
    const fileNameDisplay = document.getElementById('fileNameDisplay');

    if (file.size > maxSize) {
        showError('File quá lớn (tối đa 1MB)');
        event.target.value = '';
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const text = e.target.result;
        document.getElementById('codeEditor').value = text;
        if (fileNameDisplay) fileNameDisplay.textContent = file.name;
        showSuccess('Đã tải file vào trình soạn thảo');
    };
    reader.onerror = function() {
        showError('Không thể đọc file');
    };
    reader.readAsText(file);
}

// Get code
function getCode() {
    return document.getElementById('codeEditor').value;
}

function openRequirementsModal() {
    const modalElement = document.getElementById('requirementsModal');
    if (!modalElement) {
        showError('Không tìm thấy hộp nhập đề bài');
        return;
    }

    const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
    modal.show();
    setTimeout(() => {
        const input = document.getElementById('requirementsInput');
        if (input) input.focus();
    }, 150);
}

async function handleRequirementsAnalyze() {
    const requirements = document.getElementById('requirementsInput')?.value.trim() || '';
    if (!requirements) {
        showError('Vui lòng nhập đề bài trước khi phân tích');
        return;
    }

    const modalElement = document.getElementById('requirementsModal');
    if (modalElement) {
        const modal = bootstrap.Modal.getInstance(modalElement);
        if (modal) modal.hide();
    }

    await handleAnalyze(requirements);
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
            showCompileResult(data);
        } else {
            showError(data.error || 'Biên dịch thất bại');
            showCompileResult(data);
        }
    } catch (error) {
        hideLoading('compileSpinner');
        showError('Lỗi kết nối: ' + error.message);
    }
}

function showCompileResult(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    if (!resultsContainer) return;

    let html = '';
    if (data.success) {
        html = `
            <div class="alert alert-success alert-custom">✓ Biên dịch thành công</div>
            ${data.message ? `<div class="mb-2"><strong>Thông báo:</strong> ${escapeHtml(data.message)}</div>` : ''}
            ${data.executable ? `<div><strong>Executable:</strong> ${escapeHtml(data.executable)}</div>` : ''}
            ${data.output ? `<pre class="mt-3 p-3 bg-dark text-light rounded">${escapeHtml(data.output)}</pre>` : ''}
        `;
    } else {
        html = `
            <div class="alert alert-danger alert-custom">✗ Biên dịch thất bại</div>
            ${data.error ? `<pre class="mt-3 p-3 bg-dark text-light rounded">${escapeHtml(data.error)}</pre>` : ''}
            ${data.output ? `<pre class="mt-3 p-3 bg-dark text-light rounded">${escapeHtml(data.output)}</pre>` : ''}
        `;
    }

    resultsContainer.innerHTML = html;
}

async function handleRun() {
    const code = getCode();
    if (!code.trim()) {
        showError('Vui lòng nhập mã C');
        return;
    }

    const testCases = getTestCases();
    const inputData = testCases.length > 0 ? (testCases[0].input || '') : '';

    showLoading('runSpinner');
    try {
        const response = await fetch(`${API_BASE_URL}/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, input: inputData })
        });

        const data = await response.json();
        hideLoading('runSpinner');

        showRunResult(data);
        if (data.success) {
            showSuccess('✓ Chạy chương trình thành công');
        } else {
            showError(data.error || 'Chạy chương trình thất bại');
        }
    } catch (error) {
        hideLoading('runSpinner');
        showError('Lỗi kết nối: ' + error.message);
    }
}

function showRunResult(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    if (!resultsContainer) return;

    let html = '';
    if (data.success) {
        html = `
            <div class="alert alert-success alert-custom">✓ Chạy chương trình thành công</div>
            ${data.output ? `<div class="mb-2"><strong>Output:</strong></div><pre class="mt-2 p-3 bg-dark text-light rounded">${escapeHtml(data.output)}</pre>` : '<div class="text-muted">Chương trình không in ra gì.</div>'}
            ${data.error ? `<div class="mt-3"><strong>Stderr:</strong><pre class="mt-2 p-3 bg-dark text-light rounded">${escapeHtml(data.error)}</pre></div>` : ''}
        `;
    } else {
        html = `
            <div class="alert alert-danger alert-custom">✗ Chạy chương trình thất bại</div>
            ${data.error ? `<div class="mb-2"><strong>Lỗi:</strong></div><pre class="mt-2 p-3 bg-dark text-light rounded">${escapeHtml(data.error)}</pre>` : ''}
            ${data.compile_output ? `<div class="mt-3"><strong>Compile output:</strong><pre class="mt-2 p-3 bg-dark text-light rounded">${escapeHtml(data.compile_output)}</pre></div>` : ''}
        `;
    }

    resultsContainer.innerHTML = html;
}

function escapeHtml(text) {
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// Handle Analyze
async function handleAnalyze(requirements = '') {
    const code = getCode();
    const testcases = getTestCases();

    if (!code.trim()) {
        showError('Vui lòng nhập mã C');
        return;
    }

    showLoading('analyzeSpinner');
    try {
        const aiProviderEl = document.getElementById('aiProviderSelect');
        const aiProvider = aiProviderEl ? aiProviderEl.value : 'gemini';

        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, testcases, requirements, ai_provider: aiProvider })
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

        // Test results - HIDDEN (only for backend processing)
        // if (data.test_results && data.test_results.length > 0) {
        //     resultHTML += '<h6 class="mt-3">Test Results:</h6>';
        //     data.test_results.forEach((test, idx) => {
        //         const status = test.passed ? '✓ PASS' : '✗ FAIL';
        //         const statusClass = test.passed ? 'passed' : 'failed';
        //         resultHTML += `<div class="test-case-result ${statusClass}">`;
        //         resultHTML += `<strong>Test ${idx + 1}: ${status}</strong><br>`;
        //         resultHTML += `Input: ${escapeHtml(test.input)}<br>`;
        //         resultHTML += `Expected: ${escapeHtml(test.expected)}<br>`;
        //         resultHTML += `Actual: ${escapeHtml(test.actual)}`;
        //         resultHTML += '</div>';
        //     });
        // }

        // AI Suggestions
        // AI Suggestions / Classification
            if (data.classification) {
                const cls = data.classification;
                // Show localized Vietnamese name if provided by backend
                const name = cls.bug_type_name || cls.bug_type_id || 'Unknown';
                resultHTML += '<div class="suggestion-box mt-3">';
                resultHTML += '<h6>🔎 Phân loại lỗi (AI):</h6>';
                resultHTML += `<div class="suggestion-text"><strong>${escapeHtml(name)}</strong></div>`;
                resultHTML += '</div>';
            }

        if (data.ai_analysis) {
            resultHTML += '<div class="suggestion-box mt-3">';
            resultHTML += '<h6>💡 Phân tích & Gợi ý sửa (AI):</h6>';
            // Format with line breaks and preserve whitespace for better readability
            const formattedAnalysis = escapeHtml(data.ai_analysis)
                .replace(/\n\n/g, '</p><p>')
                .replace(/\n/g, '<br>');
            resultHTML += `<div class="suggestion-text" style="white-space: pre-wrap; word-wrap: break-word;"><p>${formattedAnalysis}</p></div>`;
            resultHTML += '</div>';
        } else if (data.ai_suggestions) {
            resultHTML += '<div class="suggestion-box mt-3">';
            resultHTML += '<h6>💡 Gợi ý từ AI:</h6>';
            const formattedSuggestions = escapeHtml(data.ai_suggestions)
                .replace(/\n\n/g, '</p><p>')
                .replace(/\n/g, '<br>');
            resultHTML += `<div class="suggestion-text" style="white-space: pre-wrap; word-wrap: break-word;"><p>${formattedSuggestions}</p></div>`;
            resultHTML += '</div>';
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

// Check User Authentication
// Check authentication and redirect if not logged in
async function checkUserAuthAndRedirect() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/check`, {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (!data.authenticated) {
            // Not logged in, redirect to login page
            window.location.href = 'auth.html';
        }
    } catch (error) {
        console.error('Auth check error:', error);
        // On error, redirect to login to be safe
        window.location.href = 'auth.html';
    }
}

async function checkUserAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/check`, {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.authenticated) {
            // User is logged in
            document.getElementById('loginLink').style.display = 'none';
            document.getElementById('userDisplay').style.display = 'inline';
            document.getElementById('username').textContent = data.username;
            document.getElementById('logoutBtn').style.display = 'inline-block';
        } else {
            // User is not logged in
            document.getElementById('loginLink').style.display = 'inline-block';
            document.getElementById('userDisplay').style.display = 'none';
            document.getElementById('logoutBtn').style.display = 'none';
        }
    } catch (error) {
        console.error('Error checking auth:', error);
    }
}

// Setup Logout
function setupLogout() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function() {
            try {
                const response = await fetch(`${API_BASE_URL}/auth/logout`, {
                    method: 'POST',
                    credentials: 'include'
                });
                const data = await response.json();
                
                if (data.success) {
                    // Redirect to login page
                    window.location.href = 'auth.html';
                }
            } catch (error) {
                console.error('Logout error:', error);
            }
        });
    }
}
