"""Defines the schema for the Memberships table in our DB."""

from sqlalchemy import Column, ForeignKey, Integer, func, String, 
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import BASE

class Position(BASE):
    """
    Specifies a mapping between a Position as a Python object and the
    Positions table in our DB. A position is the title a user holds 
    in the club that the user is a member to. 
    """

    __tablename__ = 'positions'

    identifier = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)

    def to_dict(self):
        """Returns a dict representation of a position.
        """
        position_info = {
            'id' : self.identifier,
            'name' : self.name
        }
