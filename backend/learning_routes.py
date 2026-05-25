"""
Interactive Learning Routes
Các endpoints cho học tập interactively
"""
from flask import Blueprint, request, jsonify, current_app
from db_manager import DatabaseManager
from models import Attempt, AttemptStep
from bug_taxonomy import BUG_TAXONOMY
from datetime import datetime
import json

interactive_bp = Blueprint('interactive', __name__, url_prefix='/api/interactive')


def get_services():
    """Lấy các services từ app context"""
    return {
        'analyzer': current_app.analyzer,
        'db': current_app.db,
        'hint_service': current_app.hint_service
    }


@interactive_bp.route('/start-learning', methods=['POST'])
def start_learning():
    """
    Bắt đầu một session học tập
    AI tự động phân loại loại lỗi (không cần user chọn)
    
    Input: {
        "user_id": "user123",
        "problem_id": "prob001",
        "code": "...",
        "requirements": "...",
        "testcases": [...]
    }
    """
    try:
        services = get_services()
        db = services['db']
        hint_service = services['hint_service']
        analyzer = services['analyzer']
        ai_handler = services['ai_handler']
        
        data = request.get_json()
        
        # Validate - không cần bug_taxonomy_id từ client
        required = ['user_id', 'problem_id', 'code', 'requirements']
        if not all(k in data for k in required):
            return jsonify({'error': 'Missing required fields: user_id, problem_id, code, requirements'}), 400
        
        code = data['code']
        requirements = data['requirements']
        testcases = data.get('testcases', [])
        
        # Step 1: Phân tích code (compile + test)
        analysis_result = analyzer.analyze(code, testcases)
        
        # Step 2: Nếu không compile được, trả về lỗi
        if not analysis_result.get('compile_status', {}).get('success'):
            return jsonify({
                'success': False,
                'error': 'Compilation failed',
                'compile_error': analysis_result.get('compile_status', {}).get('error'),
                'errors': analysis_result.get('errors', [])
            }), 400
        
        # Step 3: Phân loại lỗi tự động bằng AI
        # Chuẩn bị test_results cho classifier
        test_results_for_classification = []
        if analysis_result.get('test_results'):
            test_results_for_classification = analysis_result['test_results']
        
        classification = ai_handler.classify_bug_type(
            code,
            requirements,
            test_results_for_classification
        )
        
        bug_type_id = classification.get('bug_type_id', 'CF001')
        bug_type_name = classification.get('bug_type_name', 'Unknown')
        
        # Step 4: Tạo attempt
        attempt = Attempt(
            user_id=data['user_id'],
            problem_id=data['problem_id'],
            original_code=code,
            bug_type=bug_type_name
        )
        
        # Lưu vào database
        attempt_id = db.save_attempt(attempt)
        
        # Step 5: Phân tích code và tạo hints
        analysis = hint_service.analyze_and_create_hints(
            code,
            bug_type_name,
            bug_type_id,
            requirements,
            testcases
        )
        
        # Lưu step đầu tiên (start)
        step = AttemptStep(1, 'analysis')
        step.code_before = code
        db.save_step(attempt_id, step)
        
        return jsonify({
            'success': True,
            'attempt_id': attempt_id,
            'bug_taxonomy_id': bug_type_id,
            'bug_type_name': bug_type_name,
            'bug_type_description': classification.get('bug_type_description', ''),
            'bug_type_evidence': classification.get('evidence', []),
            'root_cause': classification.get('root_cause', ''),
            'confidence': classification.get('confidence', 0),
            'analysis': analysis,
            'initial_hints': analysis.get('hints', []),
            'test_results': analysis_result.get('test_results', [])
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500


@interactive_bp.route('/get-hint', methods=['POST'])
def get_hint():
    """
    Lấy gợi ý tiếp theo
    
    Input: {
        "attempt_id": 1,
        "hint_level": 1,  # 1, 2, 3
        "test_case": {"input": "...", "expected_output": "..."},
        "error_info": {"actual_output": "..."}
    }
    """
    try:
        services = get_services()
        db = services['db']
        hint_service = services['hint_service']
        
        data = request.get_json()
        attempt_id = data.get('attempt_id')
        hint_level = data.get('hint_level', 1)
        
        # Lấy attempt
        attempt_data = db.get_attempt(attempt_id)
        if not attempt_data:
            return jsonify({'error': 'Attempt not found'}), 404
        
        # Lấy gợi ý từ service
        hint_result = hint_service.get_next_hint(
            attempt_data['current_code'],
            attempt_data['bug_type'],
            data.get('bug_taxonomy_id', 'CF001'),
            hint_level,
            data.get('test_case', {}),
            data.get('error_info', {})
        )
        
        # Lưu step
        steps = db.get_attempt_steps(attempt_id)
        step = AttemptStep(len(steps) + 1, 'view_hint')
        step.hint_id = f"hint_level_{hint_level}"
        step.hint_text = hint_result.get('hint_text', '')
        db.save_step(attempt_id, step)
        
        # Update attempt
        attempt_data_updated = dict(attempt_data)
        attempt_data_updated['current_hint_index'] = hint_level
        hints_viewed = json.loads(attempt_data.get('hints_viewed', '[]') or '[]')
        hints_viewed.append(f"level_{hint_level}")
        attempt_data_updated['hints_viewed'] = hints_viewed
        
        attempt_obj = Attempt(
            attempt_data['user_id'],
            attempt_data['problem_id'],
            attempt_data['original_code'],
            attempt_data['bug_type']
        )
        attempt_obj.id = attempt_id
        attempt_obj.current_code = attempt_data['current_code']
        attempt_obj.hints_viewed = hints_viewed
        attempt_obj.current_hint_index = hint_level
        attempt_obj.tests_passed = attempt_data['tests_passed']
        attempt_obj.tests_total = attempt_data['tests_total']
        attempt_obj.is_solved = bool(attempt_data['is_solved'])
        db.update_attempt(attempt_obj)
        
        return jsonify({
            'success': True,
            'hint': hint_result,
            'step_number': len(steps) + 1
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500


@interactive_bp.route('/modify-code', methods=['POST'])
def modify_code():
    """
    Người dùng sửa code
    
    Input: {
        "attempt_id": 1,
        "new_code": "...",
        "testcases": [...]
    }
    """
    try:
        services = get_services()
        db = services['db']
        analyzer = services['analyzer']
        
        data = request.get_json()
        attempt_id = data.get('attempt_id')
        new_code = data.get('new_code', '')
        test_cases = data.get('testcases', [])
        
        # Lấy attempt
        attempt_data = db.get_attempt(attempt_id)
        if not attempt_data:
            return jsonify({'error': 'Attempt not found'}), 404
        
        # Chạy testcases
        test_results = []
        passed = 0
        
        for i, tc in enumerate(test_cases):
            run_result = analyzer.run(new_code, tc.get('input', ''))
            
            test_result = {
                'testcase': i + 1,
                'passed': False,
                'input': tc.get('input', ''),
                'expected': tc.get('expected_output', ''),
                'actual': run_result.get('output', '') if run_result.get('success') else '',
                'error': run_result.get('error', '')
            }
            
            if run_result.get('success'):
                actual = run_result['output'].strip()
                expected = tc.get('expected_output', '').strip()
                test_result['passed'] = actual == expected
                if test_result['passed']:
                    passed += 1
            
            test_results.append(test_result)
        
        # Save step
        steps = db.get_attempt_steps(attempt_id)
        step = AttemptStep(len(steps) + 1, 'modify_code')
        step.code_before = attempt_data.get('current_code', '')
        step.code_after = new_code
        step.test_results = {
            'passed': passed,
            'total': len(test_cases),
            'details': test_results
        }
        db.save_step(attempt_id, step)
        
        # Update attempt
        attempt_obj = Attempt(
            attempt_data['user_id'],
            attempt_data['problem_id'],
            attempt_data['original_code'],
            attempt_data['bug_type']
        )
        attempt_obj.id = attempt_id
        attempt_obj.current_code = new_code
        attempt_obj.tests_passed = passed
        attempt_obj.tests_total = len(test_cases)
        attempt_obj.is_solved = (passed == len(test_cases) and len(test_cases) > 0)
        attempt_obj.hints_viewed = json.loads(attempt_data.get('hints_viewed', '[]') or '[]')
        attempt_obj.current_hint_index = attempt_data.get('current_hint_index', 0)
        
        if attempt_obj.is_solved:
            attempt_obj.completed_time = datetime.now()
        
        db.update_attempt(attempt_obj)
        
        return jsonify({
            'success': True,
            'test_results': test_results,
            'passed': passed,
            'total': len(test_cases),
            'is_solved': attempt_obj.is_solved,
            'step_number': len(steps) + 1
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500


@interactive_bp.route('/get-guidance', methods=['POST'])
def get_guidance():
    """
    Lấy hướng dẫn step-by-step tiếp theo
    
    Input: {
        "attempt_id": 1,
        "requirements": "...",
        "testcases": [...]
    }
    """
    try:
        services = get_services()
        db = services['db']
        hint_service = services['hint_service']
        
        data = request.get_json()
        attempt_id = data.get('attempt_id')
        
        # Lấy attempt
        attempt_data = db.get_attempt(attempt_id)
        if not attempt_data:
            return jsonify({'error': 'Attempt not found'}), 404
        
        # Lấy history
        steps = db.get_attempt_steps(attempt_id)
        
        # Tạo guidance
        guidance = hint_service.get_step_by_step_guidance(
            attempt_data['current_code'],
            data.get('requirements', ''),
            data.get('testcases', []),
            steps
        )
        
        return jsonify({
            'success': True,
            'guidance': guidance
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500


@interactive_bp.route('/get-attempt/<int:attempt_id>', methods=['GET'])
def get_attempt(attempt_id):
    """Lấy thông tin một attempt"""
    try:
        services = get_services()
        db = services['db']
        
        attempt_data = db.get_attempt(attempt_id)
        if not attempt_data:
            return jsonify({'error': 'Attempt not found'}), 404
        
        steps = db.get_attempt_steps(attempt_id)
        stats = db.get_statistics(attempt_id)
        
        return jsonify({
            'success': True,
            'attempt': attempt_data,
            'steps': steps,
            'statistics': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500


@interactive_bp.route('/get-user-attempts/<user_id>', methods=['GET'])
def get_user_attempts(user_id):
    """Lấy tất cả attempts của user"""
    try:
        services = get_services()
        db = services['db']
        
        problem_id = request.args.get('problem_id')
        attempts = db.get_user_attempts(user_id, problem_id)
        
        # Thêm statistics cho mỗi attempt
        for attempt in attempts:
            stats = db.get_statistics(attempt['id'])
            attempt['statistics'] = stats
        
        return jsonify({
            'success': True,
            'attempts': attempts
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500


@interactive_bp.route('/get-bug-taxonomy', methods=['GET'])
def get_bug_taxonomy():
    """Lấy danh sách bug taxonomy"""
    try:
        taxonomy = []
        for key, value in BUG_TAXONOMY.items():
            taxonomy.append({
                'id': value['id'],
                'name': value['name'],
                'description': value['description'],
                'examples': value.get('examples', [])[:2]  # Chỉ 2 ví dụ
            })
        
        return jsonify({
            'success': True,
            'taxonomy': taxonomy
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'type': type(e).__name__}), 500
