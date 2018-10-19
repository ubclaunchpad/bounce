"""Defines the schema for the Memberships table in our DB."""

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import Column, ForeignKey, Integer, func, String, 
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import BASE

import logging

# Defining a enum type for role allocation
role = ENUM('president', 'admin', 'member', name ='role', metadata=metadata) 

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
    role = Column(
        'role',
        role,
        nullable=False,
    )

    member = relationship('User', back_populates='clubs')
    club = relationship('Club', back_populates='members')
    created_at = Column(
        'created_at', TIMESTAMP, nullable=False, server_default=func.now())

    def to_dict(self):
        """Returns a dict representation of a Membership."""
        return {
            'user_id': self.user_id,
            'club_id': self.club_id,
            'role': self.role,
            'created_at': self.created_at,
        }

def can_insert(editor_role=None, members_role=Member):
    """
    Determines whether user can insert a memberships to the database

    Args:
        editor_role (Role): the role of the member who is deleting the membership
        members_role (Role): the role of the member who's membership is being deleted
    """
    if editor_role == 'President':
        return True
    # Admin can only insert Member memberships
    elif editor_role == 'admin' and members_role == 'member':
        return True
    else return False


def can_select(role=None):
    # All members can read all memberships
    if role == 'President' or role == 'admin' or role == 'member':
        return True
    else return False


def can_delete(user_id=None, editor_id=None, editor_role=None, members_role=None):
    # Owners can delete all memberships
    if editor_role == 'President':
        return True
    # Admins can only delete Member memberships
    if editor_role == 'admin' and members_role == 'member':
        return True
    else return True


def insert(session, club_name, user_id, editor_role=None, members_role=Member):
    """Creates a new membership that associates the given user with the given
    club.
    
    Args:
        editor_role (Role): the role of the member who is deleting the membership
        members_role (Role): the role of the member who's membership is being deleted
    """
    # For now we do nothing on conflict, but when we have roles on these
    # memberships we need to update on conflict.
    if can_insert(editor_role, members_role):
        query = f"""
            INSERT INTO memberships (user_id, club_id, role) VALUES (
                '{user_id}',
                (SELECT id FROM clubs WHERE name = '{club_name}'),
                '{members_role}'
            )
            ON CONFLICT DO NOTHING
        """
        session.execute(query)
        session.commit()
    # TODO: Ask Bruno what to output if permission denied 
    else: logging.info("db/membership.insert: User does not have permission to insert a membership")


def select(session, club_name, user_id=None, role=None):
    """
    Returns all memberships for the given club. If user_id is given, returns
    only the membership for the given user.
    """
    # All members can read all memberships
    if can_select(role):
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
    # TODO: Ask Bruno what to output if permission denied 
    else: logging.info("db/membership.select: User does not have permission to read all memberships")


def delete(session, club_name, user_id=None, editor_id=None, editor_role=None, members_role=None):
    """
    Deletes all memberships except the Presidents for the given club. If user_id is given, deletes
    only the membership for the given user.

    Args:
        editor_role (Role): the role of the member who is deleting the membership
        members_role (Role): the role of the member who's membership is being deleted
    """
    if can_delete(user_id, editor_id, editor_role, members_role):
        # TODO: this query deletes all memberships for the club without the
        # exemption of owners
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
    # TODO: Ask Bruno what to output if permission denied 
    else: logging.info("db/membership.delete: User does not have permission to delete this membership")
