from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user
from app.crud import payment_crud

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


# ==================================================
# CREATE PAYMENT
# ==================================================

@router.post(
    "/",
    response_model=schemas.PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment(
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return payment_crud.create_payment(
        payment,
        db
    )


# ==================================================
# GET PAYMENT DETAILS
# ==================================================

@router.get(
    "/{payment_id}",
    response_model=schemas.PaymentResponse,
    status_code=status.HTTP_200_OK
)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return payment_crud.get_payment_details(
        payment_id,
        db
    )


# ==================================================
# UPDATE PAYMENT STATUS
# ==================================================

@router.put(
    "/{payment_id}/status",
    response_model=schemas.PaymentResponse,
    status_code=status.HTTP_200_OK
)
def update_payment_status(
    payment_id: int,
    payment: schemas.PaymentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return payment_crud.update_payment_status(
        payment_id,
        payment,
        db
    )