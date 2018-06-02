"""Defines the schema for the Clubs table in our DB."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # pylint: disable=invalid-name


class Club(Base):
    """
    Specifies a mapping between a Club as a Python object and the Clubs table
    in our DB.
    """
    __tablename__ = 'clubs'

    # This is just an example of what a table might look like and should
    # be updated when the real schema is ready.
    identifier = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    about = Column(String, nullable=False)
    website_url = Column(String, nullable=True)


def create_tables(engine):
    """Create the Clubs table in the DB if it does not already exist.

    Args:
        engine (Engine): the engine to use for interacting with the DB
    """
    Base.metadata.create_all(engine)
