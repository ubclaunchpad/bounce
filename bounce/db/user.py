"""Defines the schema for the Users table in our DB."""

import math

from sqlalchemy import Column, Integer, String, desc, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import BASE

# The max and min number of results to return in one page.
# Used in the search method.
MAX_SIZE = 20
MIN_SIZE = 1


class User(BASE):
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
    clubs = relationship('Membership', back_populates='member')

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
    return session.query(User).filter(User.username == username).first()


def select_by_id(session, user_id):
    """
    Returns the user with the given ID or None if
    there is no such user.
    """
    return session.query(User).filter(User.identifier == user_id).first()


def search(session, query=None, page=0, size=MAX_SIZE):
    """Returns a list of clubs that contain content from the user's query"""
    # number used for offset is the
    # page number multiplied by the size of each page
    offset_num = page * size
    users = session.query(User)

    if query:
        # show clubs that have a name that matches the query
        users = users.filter(User.full_name.ilike(f'%{query}%'))
        # TODO: implement search_vector functionality:
        # users = users.filter(User.search_vector.match(query))
        # Currently search_vector column isn't working properly

    else:
        # show clubs ordered by most recently created
        users = users.order_by(desc(User.created_at))

    result_count = users.count()
    total_pages = math.ceil(result_count / size)
    users = users.limit(size).offset(offset_num)
    return users, result_count, total_pages


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