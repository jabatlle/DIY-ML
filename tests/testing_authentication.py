import unittest
from flask import Flask
from flask_pymongo import PyMongo
from authentication import auth_blueprint

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
        app.config['SECRET_KEY'] = 'test_secret_key'

        self.mongo = PyMongo(app)
        self.db = self.mongo.db
        self.users_collection = self.db.users

        app.register_blueprint(auth_blueprint)

        self.client = app.test_client()

    def tearDown(self):
        self.db.users.drop()

    def test_register(self):
        data = {'username': 'test_user', 'password': 'test_password'}
        response = self.client.post('/register', json=data)
        self.assertEqual(response.status_code, 302)  # Check if redirecting to login page

        user = self.users_collection.find_one({'username': 'test_user'})
        self.assertIsNotNone(user)  # Check if user is inserted into the database

    def test_login(self):
        # First, register a user
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post('/register', json=data)

        # Then, try to login with correct credentials
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 302)  # Check if redirecting to home page

        # Try to login with incorrect credentials
        data['password'] = 'wrong_password'
        response = self.client.post('/login', json=data)
        self.assertEqual(response.status_code, 401)  # Check if unauthorized

    def test_logout(self):
        # First, register a user
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post('/register', json=data)

        # Then, login
        self.client.post('/login', json=data)

        # Now, try to logout
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)  # Check if redirecting to login page

if __name__ == '__main__':
    unittest.main()
