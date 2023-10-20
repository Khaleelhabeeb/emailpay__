import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transaction_handler import *
import unittest
from unittest.mock import patch

class TestTransactionHandler(unittest.TestCase):

    def setUp(self):
        self.user_id = 1
        self.recipient_email = 'testuser2@example.com'
        self.amount = Decimal(100)

    @patch('transaction_handler.mysql')
    def test_send_money_success(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = [
            [(1, 1000)],
            [(2, 500)],
        ]
        mock_cursor.fetchone.return_value = (2, 500)
        response = send_money()
        self.assertEqual(response.status_code, 302)

    @patch('transaction_handler.mysql')
    def test_send_money_insufficient_balance(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = [
            [(1, 10)],
        ]
        response = send_money()
        self.assertEqual(response.status_code, 302)

    @patch('transaction_handler.mysql')
    def test_send_money_recipient_not_found(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = [
            [(1, 1000)],
        ]
        mock_cursor.fetchone.return_value = None
        response = send_money()
        self.assertEqual(response.status_code, 302)

    @patch('transaction_handler.mysql')
    def test_send_money_database_error(self, mock_mysql):
        mock_cursor = mock_mysql.connection.cursor.return_value
        mock_cursor.execute.side_effect = Exception('Database error')
        response = send_money()
        self.assertEqual(response.status_code, 302)

    def test_transaction_success(self):
        response = transaction_success()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()