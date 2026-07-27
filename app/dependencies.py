from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.oauth2 import get_current_user
from app.models import User


# ==================================================
# DATABASE DEPENDENCY
# ==================================================

DBSession = Depends(get_db)


# ==================================================
# CURRENT AUTHENTICATED USER
# ==================================================

CurrentUser = Depends(get_current_user)


# ==================================================
# OPTIONAL HELPER
# ==================================================

def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    """
    Returns the currently authenticated user.
    You can later add active/inactive user checks here.
    """
    return current_user