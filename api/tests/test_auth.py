import pytest
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException
from passlib.exc import UnknownHashError
from jose import jwt, JWTError
from ..models.models import User
from ..schemas import schemas
from ..utils.auth import (
    verify_password,
    get_password_hash,
    get_user,
    authenticate_user,
    create_access_token,
    clear_expired_tokens,
    validate_token,
    get_current_user,
    token_cache,
    SECRET_KEY,
    ALGORITHM
)


def test_verify_password_success():
    plain_password = "password"
    hashed_passsword = get_password_hash(plain_password)
    verify_password(plain_password, hashed_passsword)


def test_verify_password_failed():
    plain_password = "password"
    with pytest.raises(UnknownHashError) as exc_info:
        verify_password(plain_password, "something")

    assert exc_info


def test_get_password_hash():
    password = "password"
    hashed_password = get_password_hash(password)

    assert password != hashed_password


def test_get_user(db_session, create_user):
    result = get_user(db_session, create_user.username)

    assert result == create_user


def test_get_user_none(db_session):
    result = get_user(db_session, "user")

    assert result is None


def test_authenticate_user_success(db_session):
    username = "user"
    password = "password"
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()
    authenticate_user(db_session, username, password)


def test_authenticate_user_not_found(db_session):
    with pytest.raises(HTTPException) as exc_info:
        authenticate_user(db_session, "user", "password")

    assert exc_info.value.status_code == 404
    assert "not found." in exc_info.value.detail


def test_authenticate_user_wrong_password(db_session):
    username = "user"
    password = "password"
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db_session.add(user)
    db_session.commit()
    with pytest.raises(HTTPException) as exc_info:
        authenticate_user(db_session, username, "idk")

    assert exc_info.value.status_code == 401
    assert "Wrong password" in exc_info.value.detail


def test_create_access_token(mocker):
    mocker.patch("api.utils.auth.jwt.encode", return_value="token123")
    token = create_access_token({"sub": "testuser"})
    assert token == "token123"


def test_clear_expired_tokens():
    token_cache.clear()
    current_time = datetime.now(timezone.utc)
    token_cache["token1"] = datetime(2020, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    token_cache["token2"] = current_time + timedelta(minutes=5)
    clear_expired_tokens()
    assert "token1" not in token_cache
    assert "token2" in token_cache


def test_validate_token_valid():
    token_cache.clear()
    expiration_time = int((datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp())
    payload = {"sub": "testuser", "exp": expiration_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    token_cache[token] = datetime.fromtimestamp(expiration_time, timezone.utc)
    assert validate_token(token) == "testuser"
    token_cache.clear()


def test_validate_token_expired():
    token_cache.clear()
    expiration_time = int((datetime.now(timezone.utc) - timedelta(minutes=30)).timestamp())
    payload = {"sub": "testuser", "exp": expiration_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    token_cache[token] = datetime.fromtimestamp(expiration_time, timezone.utc)
    with pytest.raises(HTTPException) as exc_info:
        validate_token(token)
    assert exc_info.value.status_code == 401
    assert "Invalid token." in exc_info.value.detail
    token_cache.clear()


def test_validate_token_invalid_jwt(mocker):
    token_cache.clear()
    mocker.patch("api.utils.auth.jwt.decode", side_effect=JWTError)
    with pytest.raises(HTTPException) as exc_info:
        validate_token("invalid_token")
    assert exc_info.value.status_code == 401
    assert "Invalid token" in exc_info.value.detail
    token_cache.clear()


def test_validate_token_no_username():
    token_cache.clear()
    expiration_time = int((datetime.now(timezone.utc) - timedelta(minutes=30)).timestamp())
    payload = {"exp": expiration_time}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    token_cache[token] = datetime.fromtimestamp(expiration_time, timezone.utc)
    with pytest.raises(HTTPException) as exc_info:
        validate_token(token)
    assert exc_info.value.status_code == 401
    assert "Invalid token" in exc_info.value.detail
    token_cache.clear()


def test_get_current_user_success(db_session, mocker):
    user = schemas.User(username="testuser")
    mocker.patch("api.utils.auth.get_user").return_value = user
    mocker.patch("api.utils.auth.validate_token", return_value="testuser")
    result = get_current_user(db_session, "valid_token")
    assert result == user


def test_get_current_user_not_found(db_session, mocker):
    mocker.patch("api.utils.auth.get_user").return_value = None
    mocker.patch("api.utils.auth.validate_token", return_value="testuser")
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(db_session, "valid_token")

    assert exc_info.value.status_code == 404
    assert "User 'testuser' not found" in exc_info.value.detail
