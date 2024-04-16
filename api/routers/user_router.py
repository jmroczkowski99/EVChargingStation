from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from ..crud import crud
from ..schemas import schemas
from ..database.database import get_db
from ..utils.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/users/",
    response_model=schemas.User,
    status_code=201,
    tags=["Users"],
    summary="Create a new user"
)
def create_user(
        user_data: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    logger.info(f"Attempting to create a new user with username: {user_data.username}.")
    result = crud.create_user(db=db, user_data=user_data)
    logger.info(f"Successfully created a new user with username: {user_data.username}.")
    return result


@router.put(
    "/users/me",
    response_model=schemas.User,
    status_code=200,
    tags=["Users"],
    summary="Update your user credentials"
)
def update_user(
        username: str,
        user_data: schemas.UserCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Attempting to update user '{username}' credentials.")
    if not current_user:
        logger.error("Unauthorized attempt to update user credentials.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to update user credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="Cannot update other user's credentials.")
    result = crud.update_user(db=db, username=username, user_data=user_data)
    logger.info(f"Successfully updated user '{username}' credentials.")
    return result


@router.delete(
    "/users/me",
    status_code=204,
    tags=["Users"],
    summary="Delete your user credentials"
)
def delete_user(
        username: str,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Attempting to delete user '{username}'.")
    if not current_user:
        logger.error("Unauthorized attempt to delete a user.")
        raise HTTPException(
            status_code=401,
            detail="Not authorized to delete a user.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if current_user.username != username:
        raise HTTPException(status_code=403, detail="Cannot delete other user's credentials.")
    result = crud.delete_user(db=db, username=username)
    logger.info(f"Successfully deleted user '{username}'.")
    return result
