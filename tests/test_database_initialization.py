import ast
import unittest
from pathlib import Path
from unittest.mock import Mock


class DatabaseInitializationTest(unittest.TestCase):
    def run_handler(self, existing_user):
        module = ast.parse(Path('api_views/main.py').read_text())
        function = next(
            node for node in module.body
            if isinstance(node, ast.FunctionDef) and node.name == 'populate_db'
        )
        namespace = {
            'db': Mock(),
            'User': Mock(),
            'Response': Mock(return_value='response'),
        }
        namespace['User'].query.first.return_value = existing_user
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'api_views/main.py', 'exec'), namespace)
        response = namespace['populate_db']()
        return namespace, response

    def test_existing_users_are_not_dropped_or_reseeded(self):
        namespace, response = self.run_handler(object())

        self.assertEqual(response, 'response')
        namespace['db'].drop_all.assert_not_called()
        namespace['db'].create_all.assert_called_once_with()
        namespace['User'].init_db_users.assert_not_called()

    def test_empty_database_still_gets_seed_users(self):
        namespace, response = self.run_handler(None)

        self.assertEqual(response, 'response')
        namespace['db'].create_all.assert_called_once_with()
        namespace['User'].init_db_users.assert_called_once_with()
