"""Defines the schema for the Interests table in our DB."""

from sqlalchemy import Column, Integer, String, desc, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import BASE

class Interest(BASE):
    """
    Specifies a mapping between Interest as a Python object and the Interests table
    in our DB.
    """

    __tablename__ = 'interests'

    identifier = Column('id', Integer, primary_key=True)
    interest_name = Column('interest_name', String, nullable=False)
    
    def to_dict(self):
        """Returns a dict representation of an interest.
        """

        interest_info = {
            'id': self.identifier,
            'interest_name': self.interest_name
        }
        return interest_info

def add_interest(session, interest_name):
    """Insert an new interst in the interests table"""
    new_interest = Interest(interest_name = interest_name)
    session.add(new_interest)
    session.commit()

def update_interest(session, interest_name):
    """Update an interest in the interest"""
    interest = session.query(Interest).filter(
        Interest.interest_name == interest_name).first()

    interest.interest_name = interest_name
    
def remove_interest(session, interest_name):
    """Removed an interest from the interests table"""
    session.query(Interest).filter(
        Interest.interest_name == interest_name).delete()
    session.commit()



