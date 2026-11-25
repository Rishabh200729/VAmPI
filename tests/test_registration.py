import unittest

import jsonschema

from api_views.json_schemas import register_user_schema


class RegistrationSchemaTest(unittest.TestCase):
    def test_public_registration_rejects_privilege_properties(self):
        ordinary_registration = {
            "username": "ordinary",
            "password": "pass",
            "email": "ordinary@example.test",
        }
        jsonschema.validate(ordinary_registration, register_user_schema)

        elevated_registration = dict(ordinary_registration, admin=True)
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(elevated_registration, register_user_schema)


if __name__ == "__main__":
    unittest.main()
