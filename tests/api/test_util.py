"""Tests Bounce API utilities."""

from bounce.server.api import util


def test_validate_password__success():
    assert util.validate_password('Th1sisd!')
    assert util.validate_password('%$#@KJNlk jdfjd34657')


def test_validate_password__failure():
    assert not util.validate_password('?1Tb')  # Too short
    assert not util.validate_password('asdf!2kjnb')  # No uppercase characters
    assert not util.validate_password('5OJ@^K1!SF')  # No lowercase characters
    assert not util.validate_password('lkjOIEJROI23432')  # No symbols
    assert not util.validate_password('@#$nasdfJH UH@$$$')  # No numbers
    assert not util.validate_password('~`@#$dJn UH@$$$')  # Invalid characters


def test_validate_username__success():
    assert util.validate_username('te--st.Us3r_me')


def test_validate_username__failure():
    assert not util.validate_username('aa')  # Too short
    assert not util.validate_username('aaOIlkwje.sdleofe_-aksdw-')  # Too long
    assert not util.validate_username('a1 43g')  # Invalid characters


def test_hash_and_check_password__success():
    pw = 'this!isMy439802-pass WORD$$$'
    hashed_pw = util.hash_password(pw)

    assert isinstance(hashed_pw, str)
    assert util.check_password(pw, hashed_pw)


def test_hash_and_check_password__failure():
    pw = 'this!isMy439802-pass WORD$$$'
    wrong_pw = 'this!isMy439802-pass WORD$$ '
    hashed_pw = util.hash_password(pw)

    assert isinstance(hashed_pw, str)
    assert not util.check_password(wrong_pw, hashed_pw)


def test_create_and_check_jwt__success():
    user_id = 12345
    secret = 'test secret'
    token = util.create_jwt(user_id, secret)
    assert util.check_jwt(token, secret) == user_id


def test_create_and_check_jwt__failure():
    token = util.create_jwt(12345, 'test secret')
    assert util.check_jwt(token, 'wrong secret') is None
