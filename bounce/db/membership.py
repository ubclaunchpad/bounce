"""Defines the schema for the Memberships table in our DB."""

from sqlalchemy import Column, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import BASE
from .club import Club
from .user import User


class Membership(BASE):
    """
    Specifies a mapping between a Membership as a Python object and the
    Memberships table in our DB. A memership is simply a mapping from a user
    to a club they're a member of.
    """
    __tablename__ = 'memberships'

    identifier = Column('id', Integer, primary_key=True)
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
            'id': self.identifier,
            'user_id': self.user_id,
            'club_id': self.club_id,
            'created_at': self.created_at,
        }


def insert(session, user_id, club_id):
    """Insert a new user into the Users table."""
    membership = Membership(user_id=user_id, club_id=club_id)
    session.add(membership)
    session.commit()


def select(session, club_id, user_id):
    """
    Returns the membership for the user and club with the given IDs.
    """
    membership = session.query(Membership).filter(
        Club.identifier == club_id, User.identifier == user_id).first()
    return None if membership is None else membership.to_dict()


def delete(session, club_id, user_id):
    """Deletes the membership for the user and club with the given IDs."""
    session.query(Membership).filter_by(
        club_id=club_id, user_id=user_id).delete()
    session.commit()
