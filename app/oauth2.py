from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app import models, schemas

# ==================================================
# OAuth2 Scheme
# ==================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ==================================================
# Create Access Token
# ==================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT access token.
    """

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# ==================================================
# Verify Token
# ==================================================

def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = schemas.TokenData(email=email)

    except JWTError:
        raise credentials_exception

    return token_data


# ==================================================
# Get Current User
# ==================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    token_data = verify_access_token(
        token,
        credentials_exception
    )

    user = (
        db.query(models.User)
        .filter(models.User.email == token_data.email)
        .first()
    )

    if user is None:
        raise credentials_exception

    return user