from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas


# ==================================================
# ADD MENU ITEM
# ==================================================

def add_menu_item(
    menu_item: schemas.MenuItemCreate,
    db: Session
):

    # Check Restaurant Exists
    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == menu_item.restaurant_id)
        .first()
    )

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found."
        )

    new_item = models.MenuItem(
        restaurant_id=menu_item.restaurant_id,
        item_name=menu_item.item_name,
        description=menu_item.description,
        price=menu_item.price,
        category=menu_item.category,
        availability=menu_item.availability
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


# ==================================================
# GET ALL MENU ITEMS
# SEARCH + PAGINATION
# ==================================================

def get_all_menu_items(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str = ""
):

    items = (
        db.query(models.MenuItem)
        .filter(
            models.MenuItem.item_name.ilike(f"%{search}%")
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return items


# ==================================================
# GET MENU BY RESTAURANT
# ==================================================

def get_menu_by_restaurant(
    restaurant_id: int,
    db: Session
):

    restaurant = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.id == restaurant_id)
        .first()
    )

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found."
        )

    return (
        db.query(models.MenuItem)
        .filter(
            models.MenuItem.restaurant_id == restaurant_id
        )
        .all()
    )


# ==================================================
# UPDATE MENU ITEM
# ==================================================

def update_menu_item(
    item_id: int,
    menu_item: schemas.MenuItemUpdate,
    db: Session
):

    item = (
        db.query(models.MenuItem)
        .filter(models.MenuItem.id == item_id)
        .first()
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found."
        )

    update_data = menu_item.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


# ==================================================
# DELETE MENU ITEM
# ==================================================

def delete_menu_item(
    item_id: int,
    db: Session
):

    item = (
        db.query(models.MenuItem)
        .filter(models.MenuItem.id == item_id)
        .first()
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found."
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Menu item deleted successfully."
    }