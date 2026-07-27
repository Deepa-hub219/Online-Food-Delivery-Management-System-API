import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas


# ==================================================
# CREATE PAYMENT
# ==================================================

def create_payment(
    payment: schemas.PaymentCreate,
    db: Session
):

    # Check Order Exists
    order = (
        db.query(models.Order)
        .filter(models.Order.id == payment.order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

    # Check Payment Already Exists
    existing_payment = (
        db.query(models.Payment)
        .filter(models.Payment.order_id == payment.order_id)
        .first()
    )

    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already exists for this order."
        )

    transaction_id = str(uuid.uuid4())

    new_payment = models.Payment(
        order_id=payment.order_id,
        payment_method=payment.payment_method,
        payment_status="PENDING",
        transaction_id=transaction_id
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment


# ==================================================
# GET PAYMENT DETAILS
# ==================================================

def get_payment_details(
    payment_id: int,
    db: Session
):

    payment = (
        db.query(models.Payment)
        .filter(models.Payment.id == payment_id)
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

    return payment


# ==================================================
# UPDATE PAYMENT STATUS
# ==================================================

def update_payment_status(
    payment_id: int,
    payment_data: schemas.PaymentStatusUpdate,
    db: Session
):

    payment = (
        db.query(models.Payment)
        .filter(models.Payment.id == payment_id)
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found."
        )

    payment.payment_status = payment_data.payment_status

    db.commit()
    db.refresh(payment)

    return payment