import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.api_v1.routes.auth import authenticate_user
from app.core.security import get_password_hash
from app.db.base_class import Base
from app.models.user import User


class AuthDatabaseTests(unittest.TestCase):
    def test_authentication_uses_database_user(self):
        engine = create_engine("sqlite:///:memory:")
        TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        Base.metadata.create_all(bind=engine)

        db = TestingSessionLocal()
        user = User(username="admin", hashed_password=get_password_hash("secret123"))
        db.add(user)
        db.commit()
        db.close()

        db = TestingSessionLocal()
        user = authenticate_user(db=db, username="admin", password="secret123")
        db.close()

        self.assertIsNotNone(user)
        self.assertEqual(user.username, "admin")


if __name__ == "__main__":
    unittest.main()
