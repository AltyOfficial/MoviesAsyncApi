"""Data models."""

from datetime import datetime
import uuid
# from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from auth.db.db import db
from sqlalchemy import ForeignKey


class User(db.Model):
    """A data model for user accounts."""

    __tablename__: str = 'users'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    username = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, timezone=True, default=datetime.now)
    modified = db.Column(db.DateTime, timezone=True)

    def __repr__(self) -> str:
        return f'<User {self.username}>'

'''
    def hash_password(self) -> None:
        """
        Take the password the user entered, hash it and
        then store the hashed password in the DB.

        """
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password: str) -> bool:
        """Take a plaintext password, hash it and compare
        to the hashed password stored in the DB.
        
        :param password: The password to be checked.
        :return: The password is being returned.
        """
        return check_password_hash(self.password, password)
'''

class LoginHistory(db.Model):
    """A data model for user's login history."""

    __tablename__: str = 'auth_history'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    user_agent = db.Column(db.String)
    auth_date = db.Column(db.DateTime, timezone=True)


class Role(db.Model):
    """A data model for roles of users."""

    __tablename__ = 'roles'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'<Roles {self.name}>'


class UserRole(db.Model):
    """A data model for a table that connects
    a user with their role(s).
    
    """
    __tablename__ = 'user_role'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    user_id = db.Column(UUID(as_uuid=True), ForeignKey(User.id))
    role_id = db.Column(UUID(as_uuid=True), ForeignKey(Role.id))
