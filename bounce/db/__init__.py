"""Utilities for interacting with the DB."""

import sqlalchemy
from .club import Club


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
        f'{driver}://{user}:{password}@{host}:{port}/{db_name}',
        echo=True)


def create_missing_tables(engine):
    """Create any tables that do not already exist in the DB.

    Args:
        engine (Engine): the engine created using `create_engine()`
            used to interact with the DB
        base (declarative_base): the declarative base created using
            `sqlalchemy.ext.declarative.declarative_base()` that holds table
            metadata and mappings
    """
    Club.create_table(engine)


def get_session(engine):
    """Create a new DB session bound to the given engine.

    Args:
        engine (Engine): the engine created using `create_engine`
            used to interact with the DB
    """
    return sqlalchemy.orm.sessionmaker(bind=engine)
