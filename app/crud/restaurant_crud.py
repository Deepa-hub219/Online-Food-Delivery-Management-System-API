from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app import models, schemas


# ==================================================
# CREATE RESTAURANT
# ==================================================

def create_restaurant(
    restaurant: schemas.RestaurantCreate,
    db: Session
):

    # Check Email
    existing_email = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.email == restaurant.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant email already exists."
        )

    # Check Phone
    existing_phone = (
        db.query(models.Restaurant)
        .filter(models.Restaurant.phone == restaurant.phone)
        .first()
    )

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant phone already exists."
        )

    new_restaurant = models.Restaurant(
        restaurant_name=restaurant.restaurant_name,
        owner_name=restaurant.owner_name,
        phone=restaurant.phone,
        email=restaurant.email,
        address=restaurant.address,
        status=restaurant.status
    )

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


# ==================================================
# GET ALL RESTAURANTS
# SEARCH + PAGINATION
# ==================================================

def get_all_restaurants(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: str = ""
):

    restaurants = (
        db.query(models.Restaurant)
        .filter(
            or_(
                models.Restaurant.restaurant_name.ilike(f"%{search}%"),
                models.Restaurant.owner_name.ilike(f"%{search}%")
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return restaurants


# ==================================================
# GET RESTAURANT BY ID
# ==================================================

def get_restaurant_by_id(
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

    return restaurant


# ==================================================
# UPDATE RESTAURANT
# ==================================================

def update_restaurant(
    restaurant_id: int,
    restaurant_data: schemas.RestaurantUpdate,
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

    # Email Validation
    if restaurant_data.email:

        email_exists = (
            db.query(models.Restaurant)
            .filter(
                models.Restaurant.email == restaurant_data.email,
                models.Restaurant.id != restaurant_id
            )
            .first()
        )

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists."
            )

    # Phone Validation
    if restaurant_data.phone:

        phone_exists = (
            db.query(models.Restaurant)
            .filter(
                models.Restaurant.phone == restaurant_data.phone,
                models.Restaurant.id != restaurant_id
            )
            .first()
        )

        if phone_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone already exists."
            )

    update_data = restaurant_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(restaurant, key, value)

    db.commit()
    db.refresh(restaurant)

    return restaurant


# ==================================================
# DELETE RESTAURANT
# ==================================================

def delete_restaurant(
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

    db.delete(restaurant)
    db.commit()

    return {
        "message": "Restaurant deleted successfully."
    }