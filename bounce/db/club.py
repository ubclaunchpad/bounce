"""
Defines the schema for the Clubs table in our DB.
Also provides methods to access and edit the DB.
"""

from sqlalchemy import Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TIMESTAMP

Base = declarative_base()  # pylint: disable=invalid-name


class Club(Base):
    """
    Specifies a mapping between a Club as a Python object and the Clubs table
    in our DB.
    """
    __tablename__ = 'clubs'

    identifier = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    description = Column('description', String, nullable=False)
    website_url = Column('website_url', String, nullable=True)
    facebook_url = Column('facebook_url', String, nullable=True)
    instagram_url = Column('instagram_url', String, nullable=True)
    twitter_url = Column('twitter_url', String, nullable=True)
    created_at = Column(
    'created_at', TIMESTAMP, nullable=False, server_default=func.now())

    def to_dict(self):
        """Returns a dict representation of a club."""
        return {
            'id': self.identifier,
            'name': self.name,
            'description': self.description,
            'website_url': self.website_url,
            'facebook_url': self.facebook_url,
            'instagram_url': self.instagram_url,
            'twitter_url': self.twitter_url,
            'created_at': self.created_at,
        }


def select(session, name):
    """
    Returns the club with the given name or None if
    there is no such club.
    """
    club = session.query(Club).filter(Club.name == name).first()
    return None if club is None else club.to_dict()


def insert(session, name, description, website_url, facebook_url,
           instagram_url, twitter_url):
    """Insert a new club into the Clubs table."""
    club = Club(
        name=name,
        description=description,
        website_url=website_url,
        facebook_url=facebook_url,
        instagram_url=instagram_url,
        twitter_url=twitter_url)
    session.add(club)
    session.commit()


def update(session, name, new_name, description, website_url, facebook_url,
           instagram_url, twitter_url):
    """Updates an existing club in the Clubs table and returns the
    updated club."""
    club = session.query(Club).filter(Club.name == name).first()
    if new_name:
        club.name = new_name
    if description:
        club.description = description
    if website_url:
        club.website_url = website_url
    if facebook_url:
        club.facebook_url = facebook_url
    if instagram_url:
        club.instagram_url = instagram_url
    if twitter_url:
        club.twitter_url = twitter_url
    session.commit()
    return club.to_dict()


def delete(session, name):
    """Deletes the club with the given name."""
    session.query(Club).filter(Club.name == name).delete()
    session.commit()