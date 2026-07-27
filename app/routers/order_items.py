from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
 
from app.database import get_db
from app.dependencies import get_current_user
 
from app import schemas
from app.crud import order_item_crud
 
router = APIRouter(
    prefix="/order-items",
    tags=["Order Items"]
)
 
 
# ======================================
# Add Order Item
# ======================================
 
@router.post(
    "/",
    response_model=schemas.OrderItemResponse,
    status_code=201
)
def add_order_item(
    order_item: schemas.OrderItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return order_item_crud.add_order_item(
        order_item=order_item,
        db=db
    )
 
# ======================================
# Get All Order Items
# ======================================
 
@router.get(
    "/",
    response_model=list[schemas.OrderItemResponse]
)
def get_all_order_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return order_item_crud.get_all_order_items(
        db=db,
        skip=skip,
        limit=limit
    )
 
 
# ======================================
# Get Order Items By Order ID
# ======================================
 
@router.get(
    "/order/{order_id}",
    response_model=list[schemas.OrderItemResponse]
)
def get_order_items_by_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return order_item_crud.get_order_items_by_order(
        order_id,
        db
    )
 
 
# ======================================
# Get Order Item By ID
# ======================================
 
@router.get(
    "/{order_item_id}",
    response_model=schemas.OrderItemResponse
)
def get_order_item(
    order_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return order_item_crud.get_order_item(
        order_item_id,
        db
    )
 
 
# ======================================
# Update Order Item
# ======================================
 
@router.put(
    "/{order_item_id}",
    response_model=schemas.OrderItemResponse
)
def update_order_item(
    order_item_id: int,
    order_item: schemas.OrderItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return order_item_crud.update_order_item(
        order_item_id,
        order_item,
        db
    )
 
 
# ======================================
# Delete Order Item
# ======================================
 
@router.delete("/{order_item_id}")
def delete_order_item(
    order_item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return order_item_crud.delete_order_item(
        order_item_id,
        db
    )