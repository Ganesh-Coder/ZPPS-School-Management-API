import unittest

from app.core.security import create_access_token, verify_password, get_password_hash


class AuthSecurityTests(unittest.TestCase):
    def test_password_hash_and_verify(self):
        password = "secret123"
        hashed = get_password_hash(password)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrong", hashed))

    def test_create_access_token_contains_subject(self):
        token = create_access_token("admin")
        self.assertIsInstance(token, str)
        self.assertTrue(token.count(".") == 2)


if __name__ == "__main__":
    unittest.main()
