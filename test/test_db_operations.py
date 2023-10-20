import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_operations import *
import unittest

class TestDbOperations(unittest.TestCase):

    def setUp(self):
        self.user_id = 1
        self.email = 'testuser@example.com'

    def test_get_user_profile_by_username(self):
        user_profile = get_user_profile_by_username('testuser')
        self.assertEqual(user_profile.id, self.user_id)
        self.assertEqual(user_profile.email, self.email)

    def test_get_transaction_history(self):
        transaction_history = get_transaction_history(self.user_id)
        self.assertIsInstance(transaction_history, list)
        self.assertGreaterEqual(len(transaction_history), 0)

    def test_get_recipient_fullname_from_email(self):
        recipient_fullname = get_recipient_fullname_from_email(self.email)
        self.assertEqual(recipient_fullname, 'Test User')

if __name__ == '__main__':
    unittest.main()