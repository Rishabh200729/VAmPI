import unittest
from unittest.mock import patch

from config import vuln_app
from api_views.main import populate_db


class DatabaseInitializationTests(unittest.TestCase):
    def test_empty_database_is_initialized_and_seeded(self):
        with vuln_app.app.app_context():
            with patch('api_views.main.db.create_all') as create_all, \
                    patch('api_views.main.User.query') as user_query, \
                    patch('api_views.main.User.init_db_users') as seed_users:
                user_query.first.return_value = None

                response = populate_db()

        self.assertEqual(response.status_code, 200)
        create_all.assert_called_once_with()
        seed_users.assert_called_once_with()

    def test_existing_database_is_preserved_without_reseeding(self):
        with vuln_app.app.app_context():
            with patch('api_views.main.db.create_all') as create_all, \
                    patch('api_views.main.User.query') as user_query, \
                    patch('api_views.main.User.init_db_users') as seed_users:
                user_query.first.return_value = object()

                response = populate_db()

        self.assertEqual(response.status_code, 200)
        create_all.assert_called_once_with()
        seed_users.assert_not_called()

    def test_createdb_http_route_keeps_setup_workflow(self):
        with vuln_app.app.app_context():
            with patch('api_views.main.db.create_all'), \
                    patch('api_views.main.User.query') as user_query, \
                    patch('api_views.main.User.init_db_users'):
                user_query.first.return_value = None
                response = vuln_app.app.test_client().get('/createdb')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'Database populated.'})


if __name__ == '__main__':
    unittest.main()
