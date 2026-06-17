"""
Ứng dụng Flask chính - Backend cho hệ thống phân tích lỗi mã C
"""
from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
from datetime import timedelta
import os
from dotenv import load_dotenv
from config import get_config
from analyzer import CodeAnalyzer
from ai_handler import AIHandler
from hint_service import HintService
from utils import validate_c_syntax, detect_common_errors
from utils import sanitize_ai_response
import json

# Tải biến môi trường
load_dotenv()

app = Flask(__name__)

# Load configuration
config = get_config()
app.config.from_object(config)

# Configure session
app.permanent_session_lifetime = timedelta(hours=24)

# Enable CORS with credentials support
# Enable CORS for the frontend origins. Use supports_credentials at the top level
# so Access-Control-Allow-Credentials is correctly set for credentialed requests.
CORS(app,
     resources={r"/api/*": {
         "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
         "allow_headers": ["Content-Type"]
     }},
     supports_credentials=True)

# Khởi tạo các module
analyzer = CodeAnalyzer()
# Initialize AI handler with both Gemini and OpenRouter keys (if available)
ai_handler = AIHandler(
    api_key=app.config.get('GEMINI_API_KEY', ''),
    openrouter_key=app.config.get('OPENROUTER_API_KEY', ''),
    groq_key=app.config.get('GROQ_API_KEY', '')
)
hint_service = HintService(ai_handler)

# Log whether AI keys are present (do not print actual secrets)
print(f"[config] GEMINI_API_KEY set={bool(app.config.get('GEMINI_API_KEY'))}")
print(f"[config] OPENROUTER_API_KEY set={bool(app.config.get('OPENROUTER_API_KEY'))}")

# Khởi tạo database
from db_manager import DatabaseManager
db = DatabaseManager()

# Create test user if it doesn't exist
try:
    test_user = db.get_user_by_username('testuser')
    if not test_user:
        db.register_user('testuser', 'test@example.com', 'password123')
        print('✓ Test user created: testuser/password123')
except Exception as e:
    print(f'⚠ Error creating test user: {e}')

# Gắn services vào app context để có thể truy cập từ routes
app.analyzer = analyzer
app.ai_handler = ai_handler
app.hint_service = hint_service
app.db = db

# Import và register blueprints
from learning_routes import interactive_bp
app.register_blueprint(interactive_bp)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Kiểm tra trạng thái server"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})


@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """
    Endpoint phân tích mã C
    Input: {
        "code": "...",
        "testcases": [{"input": "...", "expected_output": "..."}]
    }
    """
    try:
        data = request.get_json()
        code = data.get('code')
        testcases = data.get('testcases', [])

        if not code:
            return jsonify({'error': 'Code is required'}), 400

        # Phân tích mã
        analysis_result = analyzer.analyze(code, testcases)

        # Chạy heuristic phát hiện lỗi tĩnh (ví dụ off-by-one, missing include...)
        static_errors = detect_common_errors(code)
        if static_errors:
            # Thêm vào errors và đánh dấu has_errors để gọi AI
            analysis_result.setdefault('errors', [])
            analysis_result['errors'].extend(static_errors)
            analysis_result['has_errors'] = True

        # Nếu có lỗi hoặc test case thất bại, dùng AI để phân loại lỗi, phân tích và gợi ý sửa
        # Chuẩn bị test_results cho classifier
        test_results_for_classification = analysis_result.get('test_results', []) or []

        # Nếu có lỗi biên dịch hoặc test fail, gọi AI
        if analysis_result.get('has_errors') or any(not tr.get('passed', False) for tr in test_results_for_classification):
            # Phân loại lỗi logic
            try:
                classification = ai_handler.classify_bug_type(code, data.get('requirements', ''), test_results_for_classification)
            except Exception:
                classification = {'bug_type_id': 'CF001', 'bug_type_name': 'Unknown', 'confidence': 0}

            # Gợi ý chi tiết (analysis + fix) từ AI
            error_message = ''
            if analysis_result.get('compile_status') and not analysis_result['compile_status'].get('success'):
                error_message = analysis_result['compile_status'].get('error', '')
            else:
                # Nếu có test failures, include a short summary
                failed_tests = [tr for tr in test_results_for_classification if not tr.get('passed', False)]
                if failed_tests:
                    err_summary = []
                    for t in failed_tests:
                        err_summary.append(f"Test {t.get('testcase')}: expected='{t.get('expected')}' actual='{t.get('actual')}'")
                    error_message = '\n'.join(err_summary)

            # Allow client to request a specific AI provider via request payload
            provider = data.get('ai_provider', 'gemini') if isinstance(data, dict) else 'gemini'
            detailed = ai_handler.get_detailed_suggestions(code, error_message, '', provider=provider)

            analysis_result['classification'] = classification
            analysis_result['ai_analysis'] = detailed

            # Persist code submission and AI analysis
            try:
                user_id = session.get('user_id') if 'user_id' in session else None
                submission_id = db.save_submission(
                    user_id,
                    None,
                    code,
                    compile_status=analysis_result.get('compile_status'),
                    test_results=analysis_result.get('test_results', []),
                    run_output=analysis_result.get('run_output', '')
                )

                sanitized = sanitize_ai_response(detailed) if isinstance(detailed, str) else None
                db.save_ai_analysis(submission_id, classification, detailed if isinstance(detailed, str) else json.dumps(detailed), sanitized)
            except Exception:
                pass

        return jsonify(analysis_result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/compile', methods=['POST'])
def compile_code():
    """Biên dịch mã C"""
    try:
        data = request.get_json()
        code = data.get('code')

        if not code:
            return jsonify({'error': 'Code is required'}), 400

        result = analyzer.compile(code)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/run', methods=['POST'])
def run_code():
    """Chạy mã C với input"""
    try:
        data = request.get_json()
        code = data.get('code')
        input_data = data.get('input', '')

        if not code:
            return jsonify({'error': 'Code is required'}), 400

        result = analyzer.run(code, input_data)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/suggestions', methods=['POST'])
def get_suggestions():
    """Lấy gợi ý từ AI"""
    try:
        data = request.get_json()
        code = data.get('code')
        error_message = data.get('error_message', '')
        output = data.get('output', '')

        if not code:
            return jsonify({'error': 'Code is required'}), 400

        provider = data.get('ai_provider', 'gemini') if isinstance(data, dict) else 'gemini'
        suggestions = ai_handler.get_detailed_suggestions(
            code, error_message, output, provider=provider
        )
        return jsonify({'suggestions': suggestions})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/check-syntax', methods=['POST'])
def check_syntax():
    """Kiểm tra cú pháp C cơ bản"""
    try:
        data = request.get_json()
        code = data.get('code')

        if not code:
            return jsonify({'error': 'Code is required'}), 400

        issues = validate_c_syntax(code)
        
        return jsonify({
            'valid': len(issues) == 0,
            'issues': issues
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/detect-errors', methods=['POST'])
def detect_errors():
    """Phát hiện lỗi logic phổ biến"""
    try:
        data = request.get_json()
        code = data.get('code')

        if not code:
            return jsonify({'error': 'Code is required'}), 400

        errors = detect_common_errors(code)
        
        return jsonify({
            'has_errors': len(errors) > 0,
            'errors': errors
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/check-gcc', methods=['GET'])
def check_gcc():
    """Kiểm tra GCC có sẵn không"""
    try:
        import subprocess
        result = subprocess.run(['gcc', '--version'], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            return jsonify({
                'gcc_available': True,
                'gcc_version': version_line
            })
        else:
            return jsonify({
                'gcc_available': False,
                'gcc_version': 'Not found'
            })
    except Exception as e:
        return jsonify({
            'gcc_available': False,
            'gcc_version': f'Error: {str(e)}'
        })


@app.route('/api/check-api', methods=['GET'])
def check_api():
    """Kiểm tra Gemini API có sẵn không"""
    try:
        api_key = app.config.get('GEMINI_API_KEY', '')
        
        if not api_key or api_key.strip() == '':
            return jsonify({
                'api_available': False,
                'api_message': 'API key not configured'
            })
        
        # Kiểm tra nếu AI handler đã khởi tạo
        if hasattr(app, 'ai_handler') and app.ai_handler:
            return jsonify({
                'api_available': True,
                'api_message': 'Gemini API configured'
            })
        else:
            return jsonify({
                'api_available': False,
                'api_message': 'AI handler not initialized'
            })
    except Exception as e:
        return jsonify({
            'api_available': False,
            'api_message': f'Error: {str(e)}'
        })


# ============ AUTHENTICATION ENDPOINTS ============

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Đăng ký user mới"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        password_confirm = data.get('password_confirm', '').strip()
        
        # Validate input
        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'Vui lòng nhập đầy đủ thông tin'}), 400
        
        if len(username) < 3:
            return jsonify({'success': False, 'error': 'Username phải từ 3 ký tự trở lên'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'error': 'Password phải từ 6 ký tự trở lên'}), 400
        
        if password != password_confirm:
            return jsonify({'success': False, 'error': 'Password không khớp'}), 400
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({'success': False, 'error': 'Email không hợp lệ'}), 400
        
        # Optional full name
        full_name = data.get('full_name', '').strip()

        # Register user
        result = db.register_user(username, email, password, full_name=full_name)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Đăng nhập user"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Vui lòng nhập username và password'}), 400
        
        # Verify password
        result = db.verify_password(username, password)
        
        if result['success']:
            # Save user_id in session
            session.permanent = True
            session['user_id'] = result['user_id']
            session['username'] = result['username']
            return jsonify({'success': True, 'username': result['username'], 'user_id': result['user_id']}), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/profile', methods=['GET'])
def get_profile():
    """Lấy thông tin profile của user đang đăng nhập"""
    try:
        from flask import session
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'error': 'Chưa đăng nhập'}), 401
        
        user = db.get_user_by_id(user_id)
        
        if user:
            return jsonify({'success': True, 'user': user}), 200
        else:
            return jsonify({'success': False, 'error': 'User không tồn tại'}), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Đăng xuất user"""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/check', methods=['GET'])
def check_auth():
    """Kiểm tra trạng thái đăng nhập"""
    try:
        from flask import session
        user_id = session.get('user_id')
        username = session.get('username')
        
        if user_id:
            return jsonify({'authenticated': True, 'user_id': user_id, 'username': username}), 200
        else:
            return jsonify({'authenticated': False}), 200
            
    except Exception as e:
        return jsonify({'authenticated': False, 'error': str(e)}), 500


# Serve frontend static files in development so frontend and backend share origin.
# This route is registered after all API routes to avoid catching `/api/*` requests.
@app.route('/')
def serve_root():
    # Serve the default frontend page directly to avoid Werkzeug's automatic
    # redirect behaviour for ambiguous routes.
    base_dir = os.path.dirname(__file__)
    frontend_dir = os.path.abspath(os.path.join(base_dir, 'frontend'))
    if not os.path.isdir(frontend_dir):
        frontend_dir = os.path.abspath(os.path.join(base_dir, '..', 'frontend'))

    print(f"[serve_root] serving learning.html from {frontend_dir}")
    print(f"[url_map] {app.url_map}")
    return send_from_directory(frontend_dir, 'learning.html')


@app.route('/<path:path>')
def serve_frontend(path):
    # Prevent this catch-all from intercepting API routes
    if path.startswith('api/'):
        return jsonify({'error': 'Not Found'}), 404

    base_dir = os.path.dirname(__file__)
    frontend_dir = os.path.abspath(os.path.join(base_dir, 'frontend'))
    if not os.path.isdir(frontend_dir):
        frontend_dir = os.path.abspath(os.path.join(base_dir, '..', 'frontend'))

    target_path = os.path.join(frontend_dir, path)
    print(f"[serve_frontend] request for '{path}' -> {target_path} exists={os.path.exists(target_path)}")
    return send_from_directory(frontend_dir, path)


if __name__ == '__main__':
    # Configure session
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    # For local development we want authentication cookies to be sent with
    # cross-origin XHR/fetch requests from the frontend served on port 8000.
    # Set SameSite=None to allow cross-site cookies for credentialed requests.
    # NOTE: In production you should use Secure cookies and restrict origins.
    if app.config.get('DEBUG', True):
        # Serve frontend from the same origin in development; Lax is sufficient
        # and avoids modern browsers rejecting cookies with SameSite=None when
        # not using Secure/HTTPS.
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        app.config['SESSION_COOKIE_SECURE'] = False
    else:
        app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
        app.config['SESSION_COOKIE_SECURE'] = True
    
    print(f"Starting Flask app in {app.config.get('ENV')} mode...")
    # Run on port 5000 to avoid conflicts with other services (e.g. nginx/docker on 8000)
    # Bind to 0.0.0.0 so the container's port mapping is reachable from the host.
    app.run(debug=app.config.get('DEBUG', True), host='0.0.0.0', port=5000)
