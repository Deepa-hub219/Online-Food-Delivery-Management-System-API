from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas
from app.utils import hash_password, verify_password
from app.oauth2 import create_access_token


# ==================================================
# REGISTER USER
# ==================================================

def register_user(user: schemas.UserCreate, db: Session):

    # Check Email
    existing_email = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    # Check Phone
    existing_phone = (
        db.query(models.User)
        .filter(models.User.phone == user.phone)
        .first()
    )

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered."
        )

    # Hash Password
    hashed_pwd = hash_password(user.password)

    # Create User
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hashed_pwd,
        address=user.address
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ==================================================
# LOGIN USER
# ==================================================

def login_user(
    user_credentials: OAuth2PasswordRequestForm,
    db: Session
):

    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    if not verify_password(
        user_credentials.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }