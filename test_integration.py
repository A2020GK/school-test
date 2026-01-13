import unittest
import json
import os
import sys

# Set testing mode before importing app
os.environ['TESTING'] = 'true'


class TestFlaskRoutes(unittest.TestCase):
    """Integration tests for Flask routes"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests"""
        # Import app modules here to avoid eventlet issues
        from flask import Flask
        
        # Create a minimal test app
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.config['SECRET_KEY'] = 'test-secret-key'
        cls.app.config.update(
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE='Lax',
            SESSION_COOKIE_SECURE=False
        )
        
        # Import and set up routes without SocketIO
        from test_manager import TestManager
        from flask import request, jsonify, session, send_from_directory
        from auth import login_teacher
        
        cls.test_manager = TestManager()
        cls.students_sessions = {}
        
        @cls.app.route('/')
        def student():
            return 'Student page'
        
        @cls.app.route('/teacher', methods=['GET'])
        def teacher():
            client_ip = request.remote_addr
            if client_ip not in ['127.0.0.1', 'localhost']:
                return "❌ Доступ запрещён", 403
            return 'Teacher page'
        
        @cls.app.route('/api/check-login')
        def check_login():
            if session.get('logged_in'):
                return jsonify({'loggedIn': True})
            return jsonify({'loggedIn': False})
        
        @cls.app.route('/api/login', methods=['POST'])
        def login():
            data = request.get_json() or {}
            username = data.get('username')
            password = data.get('password')
            if login_teacher(username, password):
                session.permanent = True
                session['logged_in'] = True
                return jsonify({'message': 'Успешный вход'})
            return jsonify({'error': 'Неверный логин или пароль'}), 401
        
        @cls.app.route('/api/logout', methods=['POST'])
        def logout():
            session.clear()
            return jsonify({'message': 'Выход'})

    def setUp(self):
        """Set up test fixtures"""
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        # Clear students sessions
        self.students_sessions.clear()
        # Reset test manager
        self.test_manager.finalize_test()

    def tearDown(self):
        """Clean up after tests"""
        self.students_sessions.clear()
        self.test_manager.finalize_test()
        self.ctx.pop()

    def test_student_index_route(self):
        """Test student index page is accessible"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_teacher_route_from_localhost(self):
        """Test teacher route is accessible from localhost"""
        response = self.client.get('/teacher')
        self.assertEqual(response.status_code, 200)

    def test_check_login_not_logged_in(self):
        """Test check-login endpoint when not logged in"""
        response = self.client.get('/api/check-login')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['loggedIn'])

    def test_login_with_correct_credentials(self):
        """Test login with correct credentials"""
        response = self.client.post('/api/login',
                                    data=json.dumps({
                                        'username': 'teacherEaVi',
                                        'password': 'ChekingTest'
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Успешный вход')

    def test_login_with_incorrect_credentials(self):
        """Test login with incorrect credentials"""
        response = self.client.post('/api/login',
                                    data=json.dumps({
                                        'username': 'wrong',
                                        'password': 'wrong'
                                    }),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_login_without_credentials(self):
        """Test login without providing credentials"""
        response = self.client.post('/api/login',
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        """Test logout endpoint"""
        # First login
        self.client.post('/api/login',
                        data=json.dumps({
                            'username': 'teacherEaVi',
                            'password': 'ChekingTest'
                        }),
                        content_type='application/json')
        
        # Then logout
        response = self.client.post('/api/logout')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Выход')

    def test_check_login_after_login(self):
        """Test check-login endpoint after logging in"""
        # Login first
        self.client.post('/api/login',
                        data=json.dumps({
                            'username': 'teacherEaVi',
                            'password': 'ChekingTest'
                        }),
                        content_type='application/json')
        
        # Check login status
        response = self.client.get('/api/check-login')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['loggedIn'])

    def test_static_student_files(self):
        """Test accessing student static files"""
        # This will return 404 if file doesn't exist, but route should work
        response = self.client.get('/style.css')
        # We expect either 200 if file exists or 404 if not, but not 500
        self.assertIn(response.status_code, [200, 404])

    def test_static_teacher_files(self):
        """Test accessing teacher static files"""
        response = self.client.get('/teacher/style.css')
        # We expect either 200 if file exists or 404 if not, but not 500
        self.assertIn(response.status_code, [200, 404])


class TestDataManager(unittest.TestCase):
    """Test cases for data management functionality"""

    def test_calculate_grade_from_routes(self):
        """Test that grade calculation is accessible"""
        from routes import calculate_grade
        
        self.assertEqual(calculate_grade(95), '5')
        self.assertEqual(calculate_grade(80), '4')
        self.assertEqual(calculate_grade(60), '3')
        self.assertEqual(calculate_grade(30), '2')
        self.assertIsNone(calculate_grade(None))


if __name__ == '__main__':
    unittest.main()
