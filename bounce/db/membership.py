"""Defines the schema for the Memberships table in our DB."""

from sqlalchemy import Column, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import BASE


class Membership(BASE):
    """
    Specifies a mapping between a Membership as a Python object and the
    Memberships table in our DB. A memership is simply a mapping from a user
    to a club they're a member of.
    """
    __tablename__ = 'memberships'
    user_id = Column(
        'user_id',
        Integer,
        ForeignKey('users.id'),
        nullable=False,
        primary_key=True)
    club_id = Column(
        'club_id',
        Integer,
        ForeignKey('clubs.id'),
        nullable=False,
        primary_key=True)
    member = relationship('User', back_populates='clubs')
    club = relationship('Club', back_populates='members')
    created_at = Column(
        'created_at', TIMESTAMP, nullable=False, server_default=func.now())

    def to_dict(self):
        """Returns a dict representation of a Membership."""
        return {
            'user_id': self.user_id,
            'club_id': self.club_id,
            'created_at': self.created_at,
        }


def insert(session, club_name, user_id):
    """Creates a new membership that associates the given user with the given
    club. """
    # For now we do nothing on conflict, but when we have roles on these
    # memberships we need to update on conflict.
    query = f"""
        INSERT INTO memberships (user_id, club_id) VALUES (
            '{user_id}',
            (SELECT id FROM clubs WHERE name = '{club_name}')
        )
        ON CONFLICT DO NOTHING
    """
    session.execute(query)
    session.commit()


def select(session, club_name, user_id=None):
    """
    Returns all memberships for the given club. If user_id is given, returns
    only the membership for the given user.
    """
    query = f"""
        SELECT users.id AS user_id,
        memberships.created_at, users.full_name, users.username FROM
        memberships INNER JOIN users ON (memberships.user_id = users.id)
        WHERE memberships.club_id IN (
            SELECT id FROM clubs WHERE name = '{club_name}'
        )
    """
    if user_id:
        query += f' AND user_id = {user_id}'
    result_proxy = session.execute(query)
    results = []
    for row in result_proxy.fetchall():
        results.append(
            {key: row[i]
             for i, key in enumerate(result_proxy.keys())})
    return results


def delete(session, club_name, user_id=None):
    """
    Deletes all memberships for the given club. If user_id is given, deletes
    only the membership for the given user.
    """
    query = f"""
        DELETE FROM memberships
        WHERE memberships.club_id IN (
            SELECT id FROM clubs WHERE name = '{club_name}'
        )
    """
    if user_id:
        query += f' AND user_id = {user_id}'
    session.execute(query)
    session.commit()
