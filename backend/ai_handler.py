"""
Module xử lý AI - Tích hợp Gemini API
"""
import requests
import json
from typing import List, Dict


class AIHandler:
    """Xử lý yêu cầu với Gemini AI"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://generativelanguage.googleapis.com/v1beta/models'
        self.model = 'gemini-1.5-flash'

    def get_suggestions(self, code: str, analysis_result: Dict) -> str:
        """Lấy gợi ý từ AI dựa trên kết quả phân tích"""
        
        errors = analysis_result.get('errors', [])
        test_results = analysis_result.get('test_results', [])

        # Tạo prompt
        prompt = self._build_prompt(code, errors, test_results)

        return self._call_gemini(prompt)

    def get_detailed_suggestions(self, code: str, error_message: str, 
                                output: str) -> str:
        """Lấy gợi ý chi tiết từ AI"""
        
        prompt = f"""Tôi có đoạn mã C có lỗi logic. Vui lòng phân tích và gợi ý cách sửa:

**Mã C:**
```c
{code}
```

**Lỗi/Output:**
{error_message or output}

**Yêu cầu:**
1. Xác định lỗi logic
2. Giải thích tại sao nó sai
3. Gợi ý cách sửa cụ thể
4. Cho ví dụ mã đúng nếu cần

Vui lòng trả lời bằng tiếng Việt, ngắn gọn và rõ ràng."""

        return self._call_gemini(prompt)

    def _build_prompt(self, code: str, errors: List[str], 
                     test_results: List[Dict]) -> str:
        """Xây dựng prompt cho Gemini"""
        
        prompt = f"""Phân tích lỗi logic trong đoạn mã C sau và gợi ý sửa:

**Mã C:**
```c
{code}
```

"""
        
        if errors:
            prompt += f"**Lỗi biên dịch:**\n"
            for error in errors:
                prompt += f"- {error}\n"
            prompt += "\n"

        if test_results:
            prompt += "**Kết quả kiểm thử:**\n"
            for result in test_results:
                status = "✓ Đúng" if result['passed'] else "✗ Sai"
                prompt += f"- Test {result['testcase']}: {status}\n"
                if not result['passed']:
                    prompt += f"  Input: {result['input']}\n"
                    prompt += f"  Expected: {result['expected']}\n"
                    prompt += f"  Actual: {result['actual']}\n"

        prompt += """\n**Yêu cầu:**
1. Xác định lỗi chính
2. Giải thích kỹ tại sao sai
3. Gợi ý sửa cụ thể
4. Nếu cần, viết lại đoạn code đúng

Trả lời bằng tiếng Việt, ngắn gọn."""

        return prompt

    def classify_bug_type(self, code: str, requirements: str, test_results: list) -> dict:
        """
        Tự động phân loại loại lỗi logic
        Return: {
            'bug_type_id': 'CF001',
            'bug_type_name': '...',
            'evidence': [...],
            'root_cause': '...',
            'confidence': 0.85
        }
        """
        from prompt_generator import PromptGenerator
        
        prompt_gen = PromptGenerator()
        prompt = prompt_gen.generate_classification_prompt(code, requirements, test_results)
        
        response_text = self._call_gemini(prompt)
        
        try:
            # Parse JSON from response
            import json
            # Tìm JSON trong response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                return result
            else:
                # Fallback: Mặc định CF001
                return {
                    'bug_type_id': 'CF001',
                    'bug_type_name': 'Conditional Logic',
                    'bug_type_description': 'Điều kiện logic sai - lỗi mặc định',
                    'evidence': ['Không thể phân loại'],
                    'root_cause': 'Không xác định',
                    'confidence': 0.5
                }
        except Exception as e:
            # Fallback nếu parse JSON lỗi
            return {
                'bug_type_id': 'CF001',
                'bug_type_name': 'Conditional Logic',
                'bug_type_description': f'Conditional Logic (fallback: {str(e)})',
                'evidence': ['Lỗi parse response'],
                'root_cause': 'Không xác định',
                'confidence': 0.3
            }

    def _call_gemini(self, prompt: str) -> str:
        """Gọi Gemini API"""
        
        if not self.api_key:
            return "API key not configured"

        try:
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            payload = {
                'contents': [{
                    'parts': [{
                        'text': prompt
                    }]
                }]
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            
            # Extract text from response
            if 'candidates' in result and len(result['candidates']) > 0:
                candidate = result['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if parts and 'text' in parts[0]:
                        return parts[0]['text']

            return "Không thể nhận được gợi ý từ AI"

        except requests.exceptions.Timeout:
            return "AI request timeout"
        except requests.exceptions.RequestException as e:
            return f"AI API error: {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
