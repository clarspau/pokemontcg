"""Testing the app."""

import unittest
from app import app, db, User, Wishlist, Collection, Like


class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""

        self.app = app.test_client()  # Create a Flask test client
        db.create_all()

    def tearDown(self):
        """Tear down the test environment."""

        db.session.remove()
        db.drop_all()

    def test_example(self):
        """Example test case."""

        response = self.app.get('/')
        # Update the expected status code based on your application behavior
        self.assertEqual(response.status_code, 302)

    def test_postgresql_config(self):
        """Test PostgreSQL configuration."""

        app.config.from_object('config_test')
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI_POSTGRESQL']
        app.config['SECRET_KEY'] = app.config['SECRET_KEY_POSTGRESQL']
        response = self.app.get('/')
        # Update the expected status code based on your application behavior
        self.assertEqual(response.status_code, 302)

    def test_homepage_route(self):
        """Test the homepage route."""

        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)  # Redirect expected

    def test_login_route(self):
        """Test the login route."""

        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        """Test the register route."""

        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
