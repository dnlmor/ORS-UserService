# tests/test_services.py
import unittest
from app.utils import hash_password, verify_password, generate_token
from app.models import User

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.password = "password"
        self.user = User(id=1, username="testuser", email="test@example.com", password=hash_password(self.password))

    def test_hash_password(self):
        hashed_password = hash_password(self.password)
        self.assertNotEqual(self.password, hashed_password)

    def test_verify_password(self):
        hashed_password = hash_password(self.password)
        self.assertTrue(verify_password(self.password, hashed_password))

    def test_generate_token(self):
        token = generate_token(self.user)
        self.assertIsNotNone(token)

if __name__ == '__main__':
    unittest.main()
