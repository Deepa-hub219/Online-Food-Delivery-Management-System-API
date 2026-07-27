from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user
from app.crud import order_crud

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# ==================================================
# PLACE ORDER
# ==================================================

@router.post(
    "/",
    response_model=schemas.OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def place_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return order_crud.place_order(
        order=order,
        current_user=current_user,
        db=db
    )


# ==================================================
# GET ALL ORDERS
# ==================================================

@router.get(
    "/",
    response_model=List[schemas.OrderResponse],
    status_code=status.HTTP_200_OK
)
def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status_filter: Optional[str] = Query(
        None,
        description="Filter by order status"
    ),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return order_crud.get_all_orders(
        db=db,
        skip=skip,
        limit=limit,
        status_filter=status_filter
    )


# ==================================================
# GET ORDER BY ID
# ==================================================

@router.get(
    "/{order_id}",
    response_model=schemas.OrderResponse,
    status_code=status.HTTP_200_OK
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return order_crud.get_order_by_id(
        order_id,
        db
    )


# ==================================================
# UPDATE ORDER STATUS
# ==================================================

@router.put(
    "/{order_id}/status",
    response_model=schemas.OrderResponse,
    status_code=status.HTTP_200_OK
)
def update_order_status(
    order_id: int,
    order_status: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return order_crud.update_order_status(
        order_id,
        order_status,
        db
    )


# ==================================================
# CANCEL ORDER
# ==================================================

@router.put(
    "/{order_id}/cancel",
    status_code=status.HTTP_200_OK
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return order_crud.cancel_order(
        order_id,
        db
    )