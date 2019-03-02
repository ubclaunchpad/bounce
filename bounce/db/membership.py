"""Defines the schema for the Memberships table in our DB."""
from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import BASE, ROLE, Roles


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
        editors_role (Role):
            the role of the member who is inserting into the membership
        members_role (Role):
            the role of the member who's membership is being added
    """
    # Presidents can insert any membership
    # Admin can only insert Member memberships
    return editors_role == Roles.president.value or \
        (editors_role == Roles.admin.value and
         members_role == Roles.member.value)


def can_select(_):
    """
    Determines whether user can select a membership from the database
    Args:
        editors_role (Role):
            the role of the member who is selecting the membership
    """
    # All members can read all memberships
    return True


def can_delete_all(editors_role):
    """
    Determines whether user can delete all memberships from the database
    """
    # Presidents can delete all memberships except other presidents
    return editors_role == Roles.president.value


def can_delete_member(editors_id, members_id, editors_role, members_role):
    """
    Determines whether user can delete a membership from the database
    Args:
        editors_id: the id of the member who is deleting the membership
        members_id: the id of the member whose membership is being deleted
        editors_role (Role):
            the role of the member who is deleting the membership
        members_role (Role):
            the role of the member whose membership is being deleted
    """
    # Anyone can delete their own membership
    # Admins can only delete Member memberships
    if editors_id == members_id:
        return True
    elif editors_role == Roles.president.value:
        return members_role != Roles.president.value
    elif editors_role == Roles.admin.value:
        return members_role == Roles.member.value
    return False


def can_update(editors_role, members_role, new_role):
    """
    Determines whether user can update a membership from the database
    Args:
        editors_role (Role):
            the role of the member who is updating the membership
        members_role (Role):
            the role of the member whose membership is being updated
        new_role (Role):
            the new role of the member
    """
    # President can update any memberships except for other presidents
    # Admins can only update members membership
    if editors_role == Roles.president.value:
        return members_role != Roles.president.value
    elif editors_role == Roles.admin.value:
        return members_role == Roles.member.value and \
            new_role != Roles.president.value
    return False


def update(session, club_name, user_id, editors_role, members_role,
           new_position, new_role):
    """
    Updates membership that asscociates the give user with the given
    club.
    """
    if not can_update(editors_role, members_role, new_role):
        raise PermissionError("Permission denied for updating membership")

    query = f"""
        UPDATE memberships
        SET role = :new_role, position = :new_position
        WHERE memberships.user_id = :user_id
        AND memberships.club_id =
            (SELECT id FROM clubs WHERE name = :club_name)
    """
    session.execute(
        query, {
            'new_role': new_role,
            'new_position': new_position,
            'user_id': user_id,
            'club_name': club_name,
        })
    session.commit()


def insert(session, club_name, user_id, editors_role, members_role, position):
    """Creates a new membership that associates the given user with the given
    club.

    Args:
        editors_role (Role):
            the role of the member who is deleting the membership
        members_role (Role):
            the role of the member who's membership is being added
    """
    if not can_insert(editors_role, members_role):
        raise PermissionError('Permission denied for inserting membership.')

    query = f"""
        INSERT INTO memberships (user_id, club_id, role, position) VALUES (
            :user_id,
            (SELECT id FROM clubs WHERE name = :club_name),
            :members_role,
            :position
        )
        ON CONFLICT DO NOTHING
    """
    session.execute(
        query, {
            'user_id': user_id,
            'club_name': club_name,
            'members_role': members_role,
            'position': position,
        })
    session.commit()


def select_all(session, club_name, editors_role):
    """
    Returns all memberships for the given club. If user_id is given, returns
    only the membership for the given user.
    """
    # All members can read all memberships
    if not can_select(editors_role):
        raise PermissionError('Permission denied for selecting membership.')

    query = f"""
        SELECT users.id AS user_id,
        memberships.created_at, memberships.position,
        memberships.role, users.full_name, users.username
        FROM memberships INNER JOIN users ON (
            memberships.user_id = users.id
        )
        WHERE memberships.club_id IN (
            SELECT id FROM clubs WHERE name = :club_name
        )
    """
    result_proxy = session.execute(query, {'club_name': club_name})
    results = []
    for row in result_proxy.fetchall():
        member_info = {}
        for i, key in enumerate(result_proxy.keys()):
            member_info[key] = row[i]
        results.append(member_info)
    return results


def select_by_club_id(session, club_id, user_id, editors_role):
    """
    Returns returns the membership for the given user of the specified club.
    """
    # All members can read all memberships
    if not can_select(editors_role):
        raise PermissionError('Permission denied for selecting membership.')

    query = f"""
        SELECT users.id AS user_id,
        memberships.created_at, memberships.position,
        memberships.role, users.full_name, users.username
        FROM memberships INNER JOIN users ON (
            memberships.user_id = users.id
        )
        WHERE memberships.club_id IN (
            SELECT id FROM clubs WHERE id = :club_id
        )
        AND user_id = :user_id
    """
    result_proxy = session.execute(query, {
        'club_id': club_id,
        'user_id': user_id,
    })
    results = []
    for row in result_proxy.fetchall():
        member_info = {}
        for i, key in enumerate(result_proxy.keys()):
            # for i, key in row:
            member_info[key] = row[i]
        results.append(member_info)
    return results


def select(session, club_name, user_id, editors_role):
    """
    Returns returns the membership for the given user of the specified club.
    """
    # All members can read all memberships
    if not can_select(editors_role):
        raise PermissionError('Permission denied for selecting membership.')

    query = f"""
        SELECT users.id AS user_id,
        memberships.created_at, memberships.position,
        memberships.role, users.full_name, users.username
        FROM memberships INNER JOIN users ON (
            memberships.user_id = users.id
        )
        WHERE memberships.club_id IN (
            SELECT id FROM clubs WHERE name = :club_name
        )
        AND user_id = :user_id
    """
    result_proxy = session.execute(query, {
        'club_name': club_name,
        'user_id': user_id,
    })
    results = []
    for row in result_proxy.fetchall():
        member_info = {}
        for i, key in enumerate(result_proxy.keys()):
            # for i, key in row:
            member_info[key] = row[i]
        results.append(member_info)
    return results


def delete_all(session, club_name, editors_role):
    """
    Deletes all memberships except the Presidents for the given club.
    Args:
        club_name: the name of the club memberships are being deleted from
        editors_role (Role):
            the role of the member who is deleting the membership
        members_role (Role):
            the role of the member who's membership is being deleted
    """
    if not can_delete_all(editors_role):
        raise PermissionError(
            'Permission denied for deleting all club memberships')

    query = f"""
        DELETE FROM memberships
        WHERE NOT memberships.role = :role
        AND memberships.club_id IN (
            SELECT id FROM clubs WHERE name = :club_name
        )
    """
    session.execute(query, {
        'role': Roles.president.value,
        'club_name': club_name,
    })
    session.commit()


def delete(session, club_name, editors_id, members_id, editors_role,
           members_role):
    """
    Deletes a specific users' membership for the given club.
    Args:
        editors_id (user_id): the id of the member deleting the membership
        members_id (user_id):
            the id of the member whose membership is being deleted
        editors_role (Role):
            the role of the member who is deleting the membership
        members_role (Role):
            the role of the member whose membership is being deleted
    """
    if not can_delete_member(editors_id, members_id, editors_role,
                             members_role):
        raise PermissionError('Permission denied for deleting user membership')

    query = f"""
    DELETE FROM memberships
    WHERE memberships.club_id IN (
        SELECT id FROM clubs WHERE name = :club_name
    )
    AND memberships.user_id = :members_id
    """

    session.execute(query, {
        'club_name': club_name,
        'members_id': members_id,
    })
    session.commit()
