import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
import unittest
import pytest

class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_test_mysql_connection(self):
        response = self.app.get('/test_mysql')
        self.assertEqual(response.status_code, 200)

    def test_register_route_get(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_register_route_post(self):
        response = self.app.post('/register', data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'fullname': 'Test User',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_route_get(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_route_post(self):
        response = self.app.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)

    def test_dashboard(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 302)

    def test_send_money_route(self):
        response = self.app.post('/send_money', data={
            'recipient_email': 'testuser@example.com',
            'amount': 100,
        })
        self.assertEqual(response.status_code, 302)

    def test_transaction_success_route(self):
        response = self.app.get('/transaction_success')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()