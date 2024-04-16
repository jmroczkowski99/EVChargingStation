from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
import logging
from ..schemas import schemas
from ..database.database import get_db
from ..utils.auth import authenticate_user, create_access_token

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/token/",
    response_model=schemas.Token,
    tags=["Token"],
    summary="Access a token by logging in"
)
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    return schemas.Token(access_token=access_token, token_type="bearer")
