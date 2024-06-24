# tests/test_schema.py
import unittest
from app import create_app
from app.models import db_session, User

class TestSchema(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        db_session.remove()

    def test_create_user(self):
        response = self.client.post('/graphql', json={'query': '''
            mutation {
                createUser(username: "testuser", email: "test@example.com", password: "password") {
                    user {
                        id
                        username
                        email
                    }
                }
            }
        '''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

    def test_login_user(self):
        # First, create a user
        self.client.post('/graphql', json={'query': '''
            mutation {
                createUser(username: "testuser", email: "test@example.com", password: "password") {
                    user {
                        id
                        username
                        email
                    }
                }
            }
        '''})
        # Then, login with the created user
        response = self.client.post('/graphql', json={'query': '''
            mutation {
                loginUser(email: "test@example.com", password: "password") {
                    user {
                        id
                        username
                        email
                    }
                    token
                }
            }
        '''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)

if __name__ == '__main__':
    unittest.main()
