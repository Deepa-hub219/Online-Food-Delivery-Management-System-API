from fastapi import HTTPException, status
from sqlalchemy.orm import Session
 
from app import models, schemas
 
 
# ======================================
# Add Order Item
# ======================================
 
def add_order_item(
    order_item: schemas.OrderItemCreate,
    db: Session
):
 
    order = db.query(models.Order).filter(
        models.Order.id == order_item.order_id
    ).first()
 
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )
 
    menu_item = db.query(models.MenuItem).filter(
        models.MenuItem.id == order_item.menu_item_id
    ).first()
 
    if menu_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found."
        )
 
    new_order_item = models.OrderItem(
        order_id=order_item.order_id,
        menu_item_id=order_item.menu_item_id,
        quantity=order_item.quantity,
        price=order_item.price
    )
 
    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)
 
    return new_order_item
 
 
# ======================================
# Get All Order Items
# ======================================
 
def get_all_order_items(
    db: Session,
    skip: int = 0,
    limit: int = 10
):
 
    return db.query(models.OrderItem).offset(skip).limit(limit).all()
 
 
# ======================================
# Get Order Items By Order ID
# ======================================
 
def get_order_items_by_order(
    order_id: int,
    db: Session
):
 
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()
 
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )
 
    return db.query(models.OrderItem).filter(
        models.OrderItem.order_id == order_id
    ).all()
 
 
# ======================================
# Get Order Item By ID
# ======================================
 
def get_order_item(
    order_item_id: int,
    db: Session
):
 
    order_item = db.query(models.OrderItem).filter(
        models.OrderItem.id == order_item_id
    ).first()
 
    if order_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found."
        )
 
    return order_item
 
 
# ======================================
# Update Order Item
# ======================================
 
def update_order_item(
    order_item_id: int,
    order_item: schemas.OrderItemUpdate,
    db: Session
):
 
    db_order_item = db.query(models.OrderItem).filter(
        models.OrderItem.id == order_item_id
    ).first()
 
    if db_order_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found."
        )
 
    update_data = order_item.model_dump(exclude_unset=True)
 
    for key, value in update_data.items():
        setattr(db_order_item, key, value)
 
    db.commit()
    db.refresh(db_order_item)
 
    return db_order_item
 
 
# ======================================
# Delete Order Item
# ======================================
 
def delete_order_item(
    order_item_id: int,
    db: Session
):
 
    order_item = db.query(models.OrderItem).filter(
        models.OrderItem.id == order_item_id
    ).first()
 
    if order_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order item not found."
        )
 
    db.delete(order_item)
    db.commit()
 
    return {
        "message": "Order item deleted successfully."
    }