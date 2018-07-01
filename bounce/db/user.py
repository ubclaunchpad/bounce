"""Defines the schema for the Users table in our DB."""

from sqlalchemy import Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TIMESTAMP

Base = declarative_base()  # pylint: disable=invalid-name


class User(Base):
    """
    Specifies a mapping between a User as a Python object and the Users table
    in our DB.
    """
    __tablename__ = 'users'

    identifier = Column('id', Integer, primary_key=True)
    full_name = Column('full_name', String, nullable=False)
    username = Column('username', String, nullable=False)
    secret = Column('secret', String, nullable=False)
    email = Column('email', String, nullable=False)
    created_at = Column(
        'created_at', TIMESTAMP, nullable=False, server_default=func.now())

    def to_dict(self):
        """Returns a dict representation of a User.
        """
        user_info = {
            'id': self.identifier,
            'full_name': self.full_name,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
        }
        return user_info


def select(session, username):
    """
    Returns the user with the given username or None if
    there is no such user.
    """
<<<<<<< HEAD
    return session.query(User).filter(User.username == username).first()
=======
    user = session.query(User).filter(User.username == username).first()
    return None if user is None else user
>>>>>>> Add user authentication


def insert(session, full_name, username, secret, email):
    """Insert a new user into the Users table."""
    user = User(
        full_name=full_name, username=username, secret=secret, email=email)
    session.add(user)
    session.commit()


def update(session, username, secret=None, full_name=None, email=None):
    """Updates an existing user in the Users table and returns the
    updated user."""
    user = session.query(User).filter(User.username == username).first()
    if full_name:
        user.full_name = full_name
    if email:
        user.email = email
    if secret:
        user.secret = secret
    session.commit()
    return user


def delete(session, username):
    """Deletes the user with the given username."""
    session.query(User).filter(User.username == username).delete()
    session.commit()
