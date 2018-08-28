"""Defines the schema for the Memberships table in our DB."""

from sqlalchemy import Column, ForeignKey, Integer, func
from sqlalchemy.types import TIMESTAMP

from . import BASE


class Membership(BASE):
    """
    Specifies a mapping between a Membership as a Python object and the
    Memberships table in our DB. A memership is simply a mapping from a user
    to a club they're a member of.
    """
    __tablename__ = 'memberships'

    identifier = Column('id', Integer, primary_key=True)
    user_id = Column(
        'user_id', Integer, ForeignKey('users.user_id'), nullable=False)
    club_id = Column(
        'club_id', Integer, ForeignKey('clubs.club_id'), nullable=False)
    created_at = Column(
        'created_at', TIMESTAMP, nullable=False, server_default=func.now())

    def to_dict(self):
        """Returns a dict representation of a Membership."""
        return {
            'id': self.identifier,
            'user_id': self.user_id,
            'club_id': self.club_id,
            'created_at': self.created_at,
        }
