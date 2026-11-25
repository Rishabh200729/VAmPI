import ast
from pathlib import Path
import unittest


class UserDebugSerializationTest(unittest.TestCase):
    def test_json_debug_omits_password_and_keeps_account_details(self):
        source = Path("models/user_model.py").read_text()
        module = ast.parse(source)
        user_class = next(
            node for node in module.body
            if isinstance(node, ast.ClassDef) and node.name == "User"
        )
        method = next(
            node for node in user_class.body
            if isinstance(node, ast.FunctionDef) and node.name == "json_debug"
        )
        namespace = {}
        exec(compile(ast.Module(body=[method], type_ignores=[]), "models/user_model.py", "exec"), namespace)
        user = type(
            "UserFixture", (),
            {"username": "name1", "password": "pass1", "email": "mail1@mail.com", "admin": False},
        )()

        result = namespace["json_debug"](user)

        self.assertEqual(
            result,
            {"username": "name1", "email": "mail1@mail.com", "admin": False},
        )
        self.assertNotIn("password", result)


if __name__ == "__main__":
    unittest.main()
