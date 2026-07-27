from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user
from app.crud import restaurant_crud

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)


# ==================================================
# CREATE RESTAURANT
# ==================================================

@router.post(
    "/",
    response_model=schemas.RestaurantResponse,
    status_code=status.HTTP_201_CREATED
)
def create_restaurant(
    restaurant: schemas.RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return restaurant_crud.create_restaurant(
        restaurant,
        db
    )


# ==================================================
# GET ALL RESTAURANTS
# SEARCH + PAGINATION
# ==================================================

@router.get(
    "/",
    response_model=List[schemas.RestaurantResponse],
    status_code=status.HTTP_200_OK
)
def get_all_restaurants(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query("", description="Search by restaurant or owner name"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return restaurant_crud.get_all_restaurants(
        db=db,
        skip=skip,
        limit=limit,
        search=search
    )


# ==================================================
# GET RESTAURANT BY ID
# ==================================================

@router.get(
    "/{restaurant_id}",
    response_model=schemas.RestaurantResponse,
    status_code=status.HTTP_200_OK
)
def get_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return restaurant_crud.get_restaurant_by_id(
        restaurant_id,
        db
    )


# ==================================================
# UPDATE RESTAURANT
# ==================================================

@router.put(
    "/{restaurant_id}",
    response_model=schemas.RestaurantResponse,
    status_code=status.HTTP_200_OK
)
def update_restaurant(
    restaurant_id: int,
    restaurant: schemas.RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return restaurant_crud.update_restaurant(
        restaurant_id,
        restaurant,
        db
    )


# ==================================================
# DELETE RESTAURANT
# ==================================================

@router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_200_OK
)
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return restaurant_crud.delete_restaurant(
        restaurant_id,
        db
    )