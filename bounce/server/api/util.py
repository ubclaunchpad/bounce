"""Utility functions unsed by Bounce endpoints."""

import hashlib
import re
from datetime import datetime, timedelta

import bcrypt
from jose import exceptions, jwt

# Regexes for validating passwords and usernames
# pylint: disable=anomalous-backslash-in-string
UPPERCASE = re.compile('[A-Z]+')
LOWERCASE = re.compile('[a-z]+')
NUMBERS = re.compile('[0-9]+')
PASSWORD_SYMBOLS = re.compile('[\.\-!@#$%^&*?_+ ]+')
USERNAME_SYMBOLS = re.compile('[\.\-_]+')

# All the regexes that a valid password must match
PASSWORD_REGEXES = [UPPERCASE, LOWERCASE, NUMBERS, PASSWORD_SYMBOLS]
USERNAME_REGEXES = [UPPERCASE, LOWERCASE, NUMBERS, USERNAME_SYMBOLS]

# Username and password length restrictions
MIN_PASSWORD_LENGTH = 8
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 20

# The lifetime of an access token issued by the Bounce API
TOKEN_LIFETIME = timedelta(days=30)


def validate_password(password):
    """Returns True if the password meets password restrictions and False
    otherwise.

    Valid passwords must:
        1. Be at least 8 characters long
        2. Contain at least one uppercase letter
        3. Contain at least one lowercase letter
        4. Contain at least one symbol
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        return False

    # Check that the password meets all requirements
    for regex in PASSWORD_REGEXES:
        matches = regex.findall(password)
        if matches:
            for match in matches:
                password = password.replace(match, '')
        else:
            return False

    # If there are characters left over it means that the password contains
    # invalid characters
    return len(password) == 0


def validate_username(username):
    """Returns True if the username meets the usernames restrictions and False
    otherwise.

    Valid usernames must:
        1. Be 3 - 20 characters long
        2. Only contain alphanumeric characters, hyphens, dots, and underscores
    """
    if len(username) < MIN_USERNAME_LENGTH or len(
            username) > MAX_USERNAME_LENGTH:
        return False

    # Check that the username has no invliad characters by removing all valid
    # and checking if there's anything left over
    for regex in USERNAME_REGEXES:
        matches = regex.findall(username)
        for match in matches:
            username = username.replace(match, '')
    return len(username) == 0


def hash_password(password):
    """Returns a secret created by hashing the user's password with some salt.
    This secret is used to securely verify the user's password when they
    log in.

    Args:
        password (str): the user's password
    """
    # SHA256 hash the password so the result of a fixed length
    # (bcrypt only handles passwords up to 76 bytes in length).
    digest = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
    # Combine the password with so that even if users have the
    # same password they won't have the same secret
    return bcrypt.hashpw(bytes(digest, 'utf-8'),
                         bcrypt.gensalt()).decode('utf-8')


def check_password(password, hashed_pw):
    """Returns True if the given string is the password that was used to
    generate the given hashed password and False otherwise.

    Args:
        password (str): the password to verify
        hashed_pw (str): the hashed password to verify the given password
            against
    """
    # SHA256 hash the password so the result of a fixed length
    # (bcrypt only handles passwords up to 76 bytes in length).
    digest = hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
    return bcrypt.checkpw(bytes(digest, 'utf-8'), bytes(hashed_pw, 'utf-8'))


def create_jwt(user_id, secret):
    """Returns a JSON Web Token that a client can use to authenticate with
    the Bounce API. The returned token will expire 30 days after it is issued.

    Args:
        user_id (int): the ID of the user to whom the token was issued
        secret (str): the secret with which to sign the token
    """
    return jwt.encode(
        {
            'id': user_id,
            'exp': datetime.now() + TOKEN_LIFETIME,
        },
        secret,
        algorithm='HS256')


def check_jwt(token, secret):
    """Returns the ID of the user the token was issued to if the token is valid
    and returns None is the token is not valid.

    Args:
        token (str): the token to verify
        secret (str): the user's secret
    """
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except exceptions.JWTError:
        return None
    return payload.get('id', None)
