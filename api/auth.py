from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            password = data.get('password', '')
            
            # 환경 변수에서 비밀번호 가져오기
            # Vercel 환경 변수: APP_PASSWORD
            correct_password = os.environ.get('APP_PASSWORD', '')
            
            # 비밀번호가 설정되지 않은 경우 (개발 환경)
            if not correct_password:
                # 개발 환경에서는 기본 비밀번호 사용 (프로덕션에서는 반드시 환경 변수 설정)
                correct_password = 'default123'
            
            # 비밀번호 검증
            if password == correct_password:
                result = {
                    'success': True,
                    'message': '인증 성공'
                }
                self.send_response(200)
            else:
                result = {
                    'success': False,
                    'message': '비밀번호가 올바르지 않습니다'
                }
                self.send_response(401)
            
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            error_result = {
                'success': False,
                'message': f'서버 오류: {str(e)}'
            }
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_result).encode('utf-8'))
    
    def do_GET(self):
        result = {'status': 'ok', 'message': 'Auth endpoint is running'}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

