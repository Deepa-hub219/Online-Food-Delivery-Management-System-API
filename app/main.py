from fastapi import FastAPI

from app.database import Base, engine

# Import Routers
from app.routers import (
    auth,
    users,
    restaurants,
    menu,
    orders,
    order_items,
    payments
)

# ==================================================
# CREATE DATABASE TABLES
# ==================================================

Base.metadata.create_all(bind=engine)

# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI(
    title="Online Food Delivery Management System API",
    description="""
    Advanced FastAPI Project

    Features:
    - JWT Authentication
    - User Management
    - Restaurant Management
    - Menu Management
    - Order Management
    - Order Items
    - Payment Module
    - Pagination
    - Search
    - SQLAlchemy ORM
    - MySQL
    """,
    version="1.0.0"
)

# ==================================================
# ROOT ENDPOINT
# ==================================================

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to Online Food Delivery Management System API",
        "version": "1.0.0",
        "developer": "Deepa Pavankumar"
    }

# ==================================================
# INCLUDE ROUTERS
# ==================================================

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(order_items.router)
app.include_router(payments.router)