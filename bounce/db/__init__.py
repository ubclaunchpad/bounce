"""Utilities for interacting with the DB."""

from enum import Enum

import sqlalchemy
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE = declarative_base()

# postgresql enum used for the memberships role column
ROLE = ENUM('President', 'Admin', 'Member', name='role')


class Roles(Enum):
    """
    Python enum used for getting the role of a club's member.
    Used to determine read/write access to the memberships table.
    """
    president = ROLE.enums[0]
    admin = ROLE.enums[1]
    member = ROLE.enums[2]


def create_engine(driver, user, password, host, port, db_name):
    """Create an Engine for interacting with the DB.

    Args:
        driver (str): the SQL driver to use
        user (str): the username to use when connecting to the DB
        password (str): the password to use when connecting to the DB
        host (str): the hostname of the DB
        port (int or str): the port the DB daemon listens on
        db_name (str): the name of the DB
    """
    return sqlalchemy.create_engine(
        f'{driver}://{user}:{password}@{host}:{port}/{db_name}', echo=True)


def get_sessionmaker(engine):
    """Create a new DB sessionmaker bound to the given engine.

    Args:
        engine (Engine): the engine created using `create_engine`
            used to interact with the DB
    """
    return sessionmaker(bind=engine)
