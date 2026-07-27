from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas


# =====================================================
# PLACE ORDER
# =====================================================

def place_order(
    order: schemas.OrderCreate,
    current_user: models.User,
    db: Session
):

    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == order.restaurant_id)
        .first()
    )

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found."
        )

    total_amount = 0

    order_items = []

    for item in order.items:

        menu = (
            db.query(models.MenuItem)
            .filter(
                models.MenuItem.id == item.menu_item_id,
                models.MenuItem.restaurant_id == order.restaurant_id
            )
            .first()
        )

        if menu is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item {item.menu_item_id} not found."
            )

        item_total = menu.price * item.quantity

        total_amount += item_total

        order_items.append({
            "menu_item_id": menu.id,
            "quantity": item.quantity,
            "price": menu.price
        })

    new_order = models.Order(
        user_id=current_user.id,
        restaurant_id=order.restaurant_id,
        total_amount=total_amount,
        order_status="PENDING"
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order_items:

        db_item = models.OrderItem(
            order_id=new_order.id,
            menu_item_id=item["menu_item_id"],
            quantity=item["quantity"],
            price=item["price"]
        )

        db.add(db_item)

    db.commit()

    return new_order


# =====================================================
# GET ALL ORDERS
# =====================================================

def get_all_orders(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    status_filter: str | None = None
):

    query = db.query(models.Order)

    if status_filter:
        query = query.filter(
            models.Order.order_status == status_filter
        )

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )


# =====================================================
# GET ORDER BY ID
# =====================================================

def get_order_by_id(
    order_id: int,
    db: Session
):

    order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

    return order


# =====================================================
# UPDATE ORDER STATUS
# =====================================================

def update_order_status(
    order_id: int,
    order_status: schemas.OrderStatusUpdate,
    db: Session
):

    order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

    order.order_status = order_status.order_status

    db.commit()
    db.refresh(order)

    return order


# =====================================================
# CANCEL ORDER
# =====================================================

def cancel_order(
    order_id: int,
    db: Session
):

    order = (
        db.query(models.Order)
        .filter(models.Order.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )

    order.order_status = "CANCELLED"

    db.commit()
    db.refresh(order)

    return {
        "message": "Order cancelled successfully."
    }