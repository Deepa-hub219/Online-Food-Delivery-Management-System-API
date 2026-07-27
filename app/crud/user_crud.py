from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas


# ==================================================
# GET USER PROFILE
# ==================================================

def get_profile(current_user: models.User):
    """
    Return the currently logged-in user's profile.
    """
    return current_user


# ==================================================
# UPDATE USER PROFILE
# ==================================================

def update_profile(
    user_data: schemas.UserUpdate,
    current_user: models.User,
    db: Session
):
    """
    Update logged-in user's profile.
    """

    # Check phone number uniqueness
    if user_data.phone:

        existing_phone = (
            db.query(models.User)
            .filter(
                models.User.phone == user_data.phone,
                models.User.id != current_user.id
            )
            .first()
        )

        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already exists."
            )

    # Update only provided fields
    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)

    return current_user