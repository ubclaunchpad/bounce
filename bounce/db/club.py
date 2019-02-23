"""
Defines the schema for the Clubs table in our DB.
Also provides methods to access and edit the DB.
"""
import math

from sqlalchemy import Column, Integer, String, desc, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from . import BASE

# The max and min number of results to return in one page.
# Used in the search method.
MAX_SIZE = 20
MIN_SIZE = 1


class Club(BASE):
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
    members = relationship('Membership', back_populates='club')

    def to_dict(self):
        """Returns a dict representation of a club."""
        return {
            'id': self.identifier,
            'name': self.name,
            'description': self.description,
            'website_url': self.website_url or '',
            'facebook_url': self.facebook_url or '',
            'instagram_url': self.instagram_url or '',
            'twitter_url': self.twitter_url or '',
            'created_at': self.created_at,
        }


def select(session, identifier): 
    """
    Returns the club with the given identifier or None if
    there is no such club.
    """
    club = session.query(Club).filter(Club.identifier == identifier).first()
    return None if club is None else club.to_dict()


def search(session, query=None, page=0, size=MAX_SIZE):
    # TODO: does query, page and size need default values if it's
    # already being set using the JSON schema?
    """Returns a list of clubs that contain content from the user's query"""
    # number used for offset is the
    # page number multiplied by the size of each page
    offset_num = page * size
    clubs = session.query(Club)

    if query:
        # show clubs that have a name that matches the query
        clubs = clubs.filter(Club.name.ilike(f'%{query}%'))
    else:
        # show clubs ordered by most recently created
        clubs = clubs.order_by(desc(Club.created_at))

    result_count = clubs.count()
    total_pages = math.ceil(result_count / size)
    clubs = clubs.limit(size).offset(offset_num)
    return clubs, result_count, total_pages


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


def update(session, identifier, new_name, description, website_url, facebook_url,
           instagram_url, twitter_url):
    """Updates an existing club in the Clubs table and returns the
    updated club."""
    club = session.query(Club).filter(Club.identifier == identifier).first()
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


def delete(session, identifier):
    """Deletes the club with the given identifier."""
    session.query(Club).filter(Club.identifier == identifier).delete()
    session.commit()
