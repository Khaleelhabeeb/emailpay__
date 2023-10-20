import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_auth import *
import unittest
from unittest.mock import patch

class TestUserAuth(unittest.TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        self.fullname = 'Test User'

    @patch('user_auth.mysql')
    def test_register_success(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = [[None]]
        mock_cursor.fetchone.return_value = None
        response = register()
        self.assertEqual(response.status_code, 302)

    @patch('user_auth.mysql')
    def test_register_user_exists(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = [[None]]
        mock_cursor.fetchone.return_value = (1, 'testuser', 'testuser@example.com', 'testpassword', 1000, 'Test User', 0, 0)
        response = register()
        self.assertEqual(response.status_code, 200)

    @patch('user_auth.mysql')
    def test_register_database_error(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = Exception('Database error')
        response = register()
        self.assertEqual(response.status_code, 200)

    @patch('user_auth.mysql')
    def test_login_success(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = [[None]]
        mock_cursor.fetchone.return_value = (1, 'testuser', 'testuser@example.com', 'testpassword', 1000, 'Test User', 0, 0)
        response = login()
        self.assertEqual(response.status_code, 302)

    @patch('user_auth.mysql')
    def test_login_invalid_credentials(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = [[None]]
        mock_cursor.fetchone.return_value = None
        response = login()
        self.assertEqual(response.status_code, 200)

    @patch('user_auth.mysql')
    def test_login_database_error(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = Exception('Database error')
        response = login()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()