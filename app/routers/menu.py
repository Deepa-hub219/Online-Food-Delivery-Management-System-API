from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.oauth2 import get_current_user
from app.crud import menu_crud

router = APIRouter(
    prefix="/menu",
    tags=["Menu"]
)


# ==================================================
# ADD MENU ITEM
# ==================================================

@router.post(
    "/",
    response_model=schemas.MenuItemResponse,
    status_code=status.HTTP_201_CREATED
)
def add_menu_item(
    menu_item: schemas.MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return menu_crud.add_menu_item(
        menu_item,
        db
    )


# ==================================================
# GET ALL MENU ITEMS
# SEARCH + PAGINATION
# ==================================================

@router.get(
    "/",
    response_model=List[schemas.MenuItemResponse],
    status_code=status.HTTP_200_OK
)
def get_all_menu_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query("", description="Search menu item"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return menu_crud.get_all_menu_items(
        db=db,
        skip=skip,
        limit=limit,
        search=search
    )


# ==================================================
# GET MENU BY RESTAURANT
# ==================================================

@router.get(
    "/restaurant/{restaurant_id}",
    response_model=List[schemas.MenuItemResponse],
    status_code=status.HTTP_200_OK
)
def get_menu_by_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return menu_crud.get_menu_by_restaurant(
        restaurant_id,
        db
    )


# ==================================================
# UPDATE MENU ITEM
# ==================================================

@router.put(
    "/{item_id}",
    response_model=schemas.MenuItemResponse,
    status_code=status.HTTP_200_OK
)
def update_menu_item(
    item_id: int,
    menu_item: schemas.MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return menu_crud.update_menu_item(
        item_id,
        menu_item,
        db
    )


# ==================================================
# DELETE MENU ITEM
# ==================================================

@router.delete(
    "/{item_id}",
    status_code=status.HTTP_200_OK
)
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return menu_crud.delete_menu_item(
        item_id,
        db
    )