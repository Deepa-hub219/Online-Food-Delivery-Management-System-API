from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.crud import auth_crud

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==================================================
# REGISTER USER
# ==================================================

@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return auth_crud.register_user(user, db)


# ==================================================
# LOGIN USER
# ==================================================

@router.post(
    "/login",
    response_model=schemas.Token
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return auth_crud.login_user(
        user_credentials,
        db
    )