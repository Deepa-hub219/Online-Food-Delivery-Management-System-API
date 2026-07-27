from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.oauth2 import get_current_user
from app.crud import user_crud

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ==================================================
# GET PROFILE
# ==================================================

@router.get(
    "/profile",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK
)
def get_profile(
    current_user: models.User = Depends(get_current_user)
):
    """
    Get logged-in user's profile.
    """
    return user_crud.get_profile(current_user)


# ==================================================
# UPDATE PROFILE
# ==================================================

@router.put(
    "/profile",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_200_OK
)
def update_profile(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update logged-in user's profile.
    """
    return user_crud.update_profile(
        user,
        current_user,
        db
    )