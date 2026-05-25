"""
Ứng dụng Flask chính - Backend cho hệ thống phân tích lỗi mã C
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config import get_config
from analyzer import CodeAnalyzer
from ai_handler import AIHandler
from hint_service import HintService
from utils import validate_c_syntax, detect_common_errors

# Tải biến môi trường
load_dotenv()

app = Flask(__name__)

# Load configuration
config = get_config()
app.config.from_object(config)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Khởi tạo các module
analyzer = CodeAnalyzer()
ai_handler = AIHandler(api_key=app.config.get('GEMINI_API_KEY', ''))
hint_service = HintService(ai_handler)

# Khởi tạo database
from db_manager import DatabaseManager
db = DatabaseManager()

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

        # Nếu có lỗi, gợi ý AI
        if analysis_result['has_errors']:
            ai_suggestions = ai_handler.get_suggestions(code, analysis_result)
            analysis_result['ai_suggestions'] = ai_suggestions

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

        suggestions = ai_handler.get_detailed_suggestions(
            code, error_message, output
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


if __name__ == '__main__':
    print(f"Starting Flask app in {app.config.get('ENV')} mode...")
    app.run(debug=app.config.get('DEBUG', True), host='127.0.0.1', port=5000)
