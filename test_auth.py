import unittest
from auth import login_teacher, TEACHER_CREDENTIALS


class TestAuth(unittest.TestCase):
    """Test cases for authentication module"""

    def test_login_with_correct_credentials(self):
        """Test login with correct username and password"""
        result = login_teacher(
            TEACHER_CREDENTIALS['username'],
            TEACHER_CREDENTIALS['password']
        )
        self.assertTrue(result)

    def test_login_with_incorrect_username(self):
        """Test login with incorrect username"""
        result = login_teacher('wrong_user', TEACHER_CREDENTIALS['password'])
        self.assertFalse(result)

    def test_login_with_incorrect_password(self):
        """Test login with incorrect password"""
        result = login_teacher(TEACHER_CREDENTIALS['username'], 'wrong_pass')
        self.assertFalse(result)

    def test_login_with_empty_username(self):
        """Test login with empty username"""
        result = login_teacher('', TEACHER_CREDENTIALS['password'])
        self.assertFalse(result)

    def test_login_with_empty_password(self):
        """Test login with empty password"""
        result = login_teacher(TEACHER_CREDENTIALS['username'], '')
        self.assertFalse(result)

    def test_login_with_none_values(self):
        """Test login with None values"""
        result = login_teacher(None, None)
        self.assertFalse(result)

    def test_login_case_sensitive_username(self):
        """Test that username is case-sensitive"""
        result = login_teacher(
            TEACHER_CREDENTIALS['username'].upper(),
            TEACHER_CREDENTIALS['password']
        )
        self.assertFalse(result)

    def test_login_case_sensitive_password(self):
        """Test that password is case-sensitive"""
        result = login_teacher(
            TEACHER_CREDENTIALS['username'],
            TEACHER_CREDENTIALS['password'].lower()
        )
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
