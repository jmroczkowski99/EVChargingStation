import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..models import models
from ..schemas import schemas
from ..database.database import get_db
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 2

token_cache: Dict[str, datetime] = {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).one_or_none()


def authenticate_user(db: Session, username: str, password: str):
    logger.info(f"Authenticating user '{username}'.")
    user = get_user(db, username)
    if not user:
        logger.warning("Authentication failed - nonexistent user.")
        raise HTTPException(status_code=404, detail="User not found.")
    if not verify_password(password, user.hashed_password):
        logger.warning("Authentication failed - wrong user.")
        raise HTTPException(status_code=401, detail="Wrong password.")
    logger.info(f"User '{username}' authenticated successfully.")
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    token_cache[encoded_jwt] = expire
    logger.info(f"Created a new token for user '{data.get('sub')}' with expiration at {expire}.")
    return encoded_jwt


def clear_expired_tokens():
    current_time = datetime.now(timezone.utc)
    keys_to_remove = [key for key, expiry in token_cache.items() if expiry < current_time]
    for key in keys_to_remove:
        del token_cache[key]
    if keys_to_remove:
        logger.info(f"Cleared {len(keys_to_remove)} expired tokens.")


def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    clear_expired_tokens()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            logger.warning("Token validation failed - no username found in token.")
            raise HTTPException(status_code=401, detail="Invalid token.")
        token_expiry = token_cache.get(token)
        if not token_expiry or token_expiry < datetime.now(timezone.utc):
            logger.warning("Token validation failed - token expired.")
            raise HTTPException(status_code=401, detail="Expired token.")
        logger.info(f"Token validated successfully for user '{username}'.")
        return username
    except JWTError:
        logger.error("Token validation failed - JWT Error.")
        raise HTTPException(status_code=401, detail="Invalid token.")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> schemas.User:
    username = validate_token(token)
    user = get_user(db, username)
    if not user:
        logger.error(f"User '{username}' not found.")
        raise HTTPException(status_code=404, detail=f"User '{username}' not found.")
    logger.info(f"Successfully retrieved user '{username}' from the token.")
    return user
