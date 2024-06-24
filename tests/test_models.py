# tests/test_models.py
import unittest
from app.models import User
from app.database import db_session

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user = User(username="testuser", email="test@example.com", password="password")

    def test_create_user(self):
        db_session.add(self.user)
        db_session.commit()
        self.assertIsNotNone(self.user.id)

    def tearDown(self):
        db_session.remove()

if __name__ == '__main__':
    unittest.main()
