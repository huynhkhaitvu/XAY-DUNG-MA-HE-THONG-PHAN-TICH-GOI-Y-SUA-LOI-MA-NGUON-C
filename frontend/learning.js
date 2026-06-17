// Interactive Learning System JavaScript

// Use explicit backend host for API paths to avoid conflicts with services on port 8000
const API_BASE_URL = `http://127.0.0.1:5000/api/interactive`;
const AUTH_API_BASE = `http://127.0.0.1:5000/api/auth`;
let currentAttemptId = null;
let currentBugTaxonomyId = null;
let originalCode = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    checkAuthentication();
    setupEventListeners();
    showStartModal();
});

// Check if user is authenticated
async function checkAuthentication() {
    try {
        const aiProviderEl = document.getElementById('aiProviderSelect');
        const aiProvider = aiProviderEl ? aiProviderEl.value : 'gemini';

        const response = await fetch(`${AUTH_API_BASE}/check`, {
            credentials: 'include'
        });
        const data = await response.json();
        
        if (data.authenticated) {
            // Get user profile
            const profileResponse = await fetch(`${AUTH_API_BASE}/profile`, {
                credentials: 'include'
            });
            const profileData = await profileResponse.json();
            
            if (profileData.success && profileData.user) {
                document.getElementById('userUsername').textContent = profileData.user.username || '-';
                document.getElementById('userEmail').textContent = profileData.user.email || '-';
            }
        } else {
            // Redirect to login
            window.location.href = 'auth.html';
        }
    } catch (error) {
        console.log('Auth check error:', error);
        window.location.href = 'auth.html';
    }
}

// Handle logout
async function handleLogout() {
    try {
        const response = await fetch(`${AUTH_API_BASE}/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        
        if (response.ok) {
            window.location.href = 'auth.html';
        }
    } catch (error) {
        console.log('Logout error:', error);
        window.location.href = 'auth.html';
    }
}

function setupEventListeners() {
    document.getElementById('hintLevel1Btn').addEventListener('click', () => getHint(1));
    document.getElementById('hintLevel2Btn').addEventListener('click', () => getHint(2));
    document.getElementById('hintLevel3Btn').addEventListener('click', () => getHint(3));
    document.getElementById('guidanceBtn').addEventListener('click', getGuidance);
    document.getElementById('testBtn').addEventListener('click', runTests);
    document.getElementById('resetBtn').addEventListener('click', resetCode);
    document.getElementById('submitBtn').addEventListener('click', submitCode);
    document.getElementById('startBtn').addEventListener('click', startLearning);
}

function showStartModal() {
    const modal = new bootstrap.Modal(document.getElementById('startModal'));
    modal.show();
}



async function startLearning() {
    const code = document.getElementById('problemCode').value;
    const requirements = document.getElementById('problemRequirements').value;
    
    if (!code) {
        alert('Vui lòng nhập code');
        return;
    }
    
    // Collect test cases
    const testcases = [];
    const testInputs = document.querySelectorAll('[name="testInput"]');
    const testOutputs = document.querySelectorAll('[name="testOutput"]');
    
    for (let i = 0; i < testInputs.length; i++) {
        if (testInputs[i].value || testOutputs[i].value) {
            testcases.push({
                input: testInputs[i].value,
                expected_output: testOutputs[i].value
            });
        }
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/start-learning`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: 'user_' + Date.now(),
                problem_id: 'prob_' + Date.now(),
                code: code,
                requirements: requirements,
                testcases: testcases,
                ai_provider: aiProvider
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentAttemptId = data.attempt_id;
            currentBugTaxonomyId = data.bug_taxonomy_id;
            originalCode = code;
            
            document.getElementById('codeEditor').value = code;
            displayAnalysis(data.analysis);
            displayInitialHints(data.initial_hints);
            
            // Close modal
            bootstrap.Modal.getInstance(document.getElementById('startModal')).hide();
        }
    } catch (error) {
        alert('Error starting learning: ' + error.message);
    }
}

async function getHint(level) {
    if (!currentAttemptId) {
        alert('Vui lòng bắt đầu session trước');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/get-hint`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                attempt_id: currentAttemptId,
                hint_level: level,
                bug_taxonomy_id: currentBugTaxonomyId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayHint(data.hint, level);
        }
    } catch (error) {
        console.error('Error getting hint:', error);
    }
}

async function getGuidance() {
    if (!currentAttemptId) {
        alert('Vui lòng bắt đầu session trước');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/get-guidance`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                attempt_id: currentAttemptId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayGuidance(data.guidance);
        }
    } catch (error) {
        console.error('Error getting guidance:', error);
    }
}

async function runTests() {
    if (!currentAttemptId) {
        alert('Vui lòng bắt đầu session trước');
        return;
    }
    
    const code = document.getElementById('codeEditor').value;
    
    try {
        // Lấy testcases từ form
        const testcases = getTestcasesFromForm();
        
        const response = await fetch(`${API_BASE_URL}/modify-code`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                attempt_id: currentAttemptId,
                new_code: code,
                testcases: testcases
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayTestResults(data.test_results);
            updateProgress(data.passed, data.total);
            
            if (data.is_solved) {
                showSuccess('🎉 Chúc mừng! Bạn đã sửa đúng lỗi!');
            }
        }
    } catch (error) {
        console.error('Error running tests:', error);
    }
}

function resetCode() {
    if (originalCode) {
        document.getElementById('codeEditor').value = originalCode;
    }
}

function submitCode() {
    const code = document.getElementById('codeEditor').value;
    if (code === originalCode) {
        alert('Bạn chưa sửa gì. Hãy sửa code theo gợi ý');
    } else {
        runTests();
    }
}

function displayAnalysis(analysis) {
    const container = document.getElementById('hintContainer');
    let html = '<div class="analysis-box">';
    
    if (analysis.branches_count) {
        html += `<p><strong>Số nhánh:</strong> ${analysis.branches_count}</p>`;
    }
    
    if (analysis.root_cause) {
        html += `<div class="alert alert-warning"><strong>Nguyên nhân gốc:</strong><br>${analysis.root_cause}</div>`;
    }
    
    if (analysis.guided_questions) {
        html += '<strong>Câu hỏi hướng dẫn:</strong><ul>';
        analysis.guided_questions.forEach((q, i) => {
            html += `<li>${q}</li>`;
        });
        html += '</ul>';
    }
    
    html += '</div>';
    container.innerHTML = html;
}

function displayInitialHints(hints) {
    const container = document.getElementById('hintContainer');
    let html = container.innerHTML + '<hr>';
    
    if (hints && hints.length > 0) {
        html += '<strong>Gợi ý khởi đầu:</strong>';
        hints.forEach((hint, i) => {
            html += `<div class="hint-box">
                <span class="hint-level">Level ${hint.level}</span>
                <div class="hint-text">${hint.hint}</div>
            </div>`;
        });
    }
    
    container.innerHTML = html;
}

function displayHint(hintData, level) {
    const container = document.getElementById('hintContainer');
    
    let html = `
        <div class="hint-box">
            <span class="hint-level">Level ${level}</span>
            <div class="hint-text">${hintData.hint_text}</div>
    `;
    
    if (hintData.follow_up_question) {
        html += `<div class="hint-question">Câu hỏi tiếp theo: ${hintData.follow_up_question}</div>`;
    }
    
    if (hintData.code_area) {
        html += `<div class="mt-2" style="font-size: 13px; color: #666;">Chú ý vùng: ${hintData.code_area}</div>`;
    }
    
    html += '</div>';
    
    container.innerHTML = html + container.innerHTML;
}

function displayGuidance(guidance) {
    const container = document.getElementById('hintContainer');
    
    let html = '<div class="guidance-box"><strong>📋 Hướng dẫn từng bước:</strong>';
    
    if (guidance.current_issues) {
        html += '<div class="mt-2"><strong>Vấn đề hiện tại:</strong><ul>';
        guidance.current_issues.forEach(issue => {
            html += `<li><strong>${issue.issue}</strong> (${issue.severity})</li>`;
        });
        html += '</ul></div>';
    }
    
    if (guidance.next_step) {
        const step = guidance.next_step;
        html += `<div class="alert alert-info mt-3">
            <strong>Step ${step.step_number}:</strong> ${step.focus_area}<br>
            <em>Câu hỏi: ${step.question}</em><br>
            <strong>Gợi ý:</strong> ${step.hint}
        </div>`;
    }
    
    html += '</div>';
    container.innerHTML = html + container.innerHTML;
}

function displayTestResults(results) {
    const container = document.getElementById('testResultsContainer');
    
    let html = '<strong>📊 Kết Quả Test:</strong>';
    
    results.forEach((result, i) => {
        const status = result.passed ? 'passed' : 'failed';
        const icon = result.passed ? '✓' : '✗';
        
        html += `
            <div class="test-result ${status}">
                <strong>${icon} Test ${result.testcase}:</strong>
                <div style="margin-top: 5px; font-size: 13px;">
                    Input: ${escapeHtml(result.input)}<br>
                    Expected: ${escapeHtml(result.expected)}<br>
                    Actual: ${escapeHtml(result.actual)}
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function updateProgress(passed, total) {
    const percent = (passed / total * 100).toFixed(0);
    
    document.getElementById('progressInfo').textContent = `${passed}/${total} tests passed`;
    document.getElementById('progressBar').style.width = percent + '%';
    
    if (passed === total && total > 0) {
        document.getElementById('progressBar').classList.add('bg-success');
    }
}

function getTestcasesFromForm() {
    // Tạm thời return empty, cần lấy từ form
    return [];
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showSuccess(message) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show';
    alert.innerHTML = `${message} <button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    document.body.prepend(alert);
}
