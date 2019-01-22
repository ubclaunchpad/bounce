"""Defines the schema for the Memberships table in our DB."""
from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import BASE, ROLE, PermissionError, Roles


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
        ROLE,
        nullable=False,
    )
    position = Column('position', String, nullable=False)

    member = relationship('User', back_populates='clubs')
    club = relationship('Club', back_populates='members')
    created_at = Column(
        'created_at', TIMESTAMP, nullable=False, server_default=func.now())

    def to_dict(self):
        """Returns a dict representation of a Membership."""
        return {
            'user_id': self.user_id,
            'club_id': self.club_id,
            'position': self.position,
            'role': self.role,
            'created_at': self.created_at,
        }


def can_insert(editors_role, members_role):
    """
    Determines whether user can insert a membership to the database
    Args:
        editors_role (Role): the role of the member who is deleting the membership
        members_role (Role): the role of the member who's membership is being deleted
    """

    if editors_role == Roles.president:
        return True
    # Admin can only insert Member memberships
    elif editors_role == Roles.admin and members_role == Roles.member:
        return True
    else:
        return False


def can_select(editors_role):
    # All members can read all memberships
    if editors_role is None:
        return False
    else:
        return True


def can_delete_all(editors_role, members_role):
    # Owners can delete all memberships except other presidents
    if editors_role == Roles.president and members_role != Roles.president:
        return True
    else:
        return False


def can_delete_member(editors_id,
                    members_id,
                    editors_role,
                    members_role):
    # Anyone can delete their own membership
    if editors_id == members_id:
        return True
    # Presidents can delete all memberships
    elif editors_role == Roles.president and members_role != Roles.president:
        return True
    # Admins can only delete Member memberships or themselves
    elif editors_role == Roles.admin and members_role == Roles.member:
        return True
    else:
        return False


def can_update(editors_role, members_role):
    # President can update any memberships but other presidents
    if editors_role == Roles.president and members_role != Roles.president:
        return True
    # Admins can only update members membership
    elif editors_role == Roles.admin and members_role == Roles.member:
        return True
    else:
        return False


def update(session, club_name, user_id, editors_role, members_role, position,
           new_position, new_role):
    """
    Updates membership that asscociates the give user with the given
    club.
    """

    if can_update(editors_role, members_role):
        query = f"""
            UPDATE memberships
            SET role = '{new_role}', position = '{new_position}'
            WHERE memberships.user_id = '{user_id}'
            AND (SELECT id FROM clubs WHERE name = '{club_name}')
        """
        session.execute(query)
        session.commit()

    else:
        raise PermissionError("Permission denied for updating membership")


def insert(session, club_name, user_id, editors_role, members_role, position):
    """Creates a new membership that associates the given user with the given
    club.

    Args:
        editors_role (Role): the role of the member who is deleting the membership
        members_role (Role): the role of the member who's membership is being added
    """
    if can_insert(editors_role, members_role):
        query = f"""
            INSERT INTO memberships (user_id, club_id, role, position) VALUES (
                '{user_id}',
                (SELECT id FROM clubs WHERE name = '{club_name}'),
                '{members_role.value}',
                '{position}'
            )
            ON CONFLICT DO NOTHING
        """
        session.execute(query)
        session.commit()
    else:
        raise PermissionError('Permission denied for inserting membership.')


def select(session, club_name, user_id, editors_role):
    """
    Returns all memberships for the given club. If user_id is given, returns
    only the membership for the given user.
    """
    # All members can read all memberships
    if can_select(editors_role):
        query = f"""
            SELECT users.id AS user_id,
            memberships.created_at, memberships.position,
            memberships.role, users.full_name, users.username 
            FROM memberships INNER JOIN users ON (memberships.user_id = users.id)
            WHERE memberships.club_id IN (
                SELECT id FROM clubs WHERE name = '{club_name}'
            )
        """
        if user_id:
            query += f' AND user_id = {user_id}'
        result_proxy = session.execute(query)
        results = {}
        for row in result_proxy.fetchall():
            for i, key in enumerate(result_proxy.keys()):
                results[key] = row[i]
        return results
    else:
        raise PermissionError('Permission denied for selecting membership.')


def delete_all(session, club_name, editors_role, members_role):
    """
    Deletes all memberships except the Presidents for the given club.
    Args:
        club_name: the name of the club memberships are being deleted from
        editors_role (Role): the role of the member who is deleting the membership
        members_role (Role): the role of the member who's membership is being deleted
    """
    if can_delete_all(editors_role, members_role):
        query = f"""
            DELETE FROM memberships
            WHERE memberships.club_id IN (
                SELECT id FROM clubs WHERE name = '{club_name}'
            )
        """

        session.execute(query)
        session.commit()
    else:
        raise PermissionError(
            'Permission denied for deleting all club memberships')


def delete(session, club_name, editors_id, members_id, editors_role,
           members_role):
    """
    Deletes a specific users' membership for the given club.
    Args:
        editors_id (user_id): the id of the member deleting the membership
        members_id (user_id): the id of the member whose membership is being deleted
        editors_role (Role): the role of the member who is deleting the membership
        members_role (Role): the role of the member whose membership is being deleted
    """
    if can_delete_member(editors_id, members_id, editors_role, members_role):
        query = f"""
        DELETE FROM memberships
        WHERE memberships.club_id IN (
            SELECT id FROM clubs WHERE name = '{club_name}'
        )
        AND memberships.user_id = '{members_id}'
        """

        session.execute(query)
        session.commit()
    else:
        raise PermissionError('Permission denied for deleting user membership')
