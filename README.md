# 🍔 Online Food Delivery Management System API

## Project Overview

The **Online Food Delivery Management System API** is a secure and scalable RESTful web service developed using **FastAPI** and **MySQL**. It allows customers to browse restaurants, view menus, place food orders, make payments, and manage their profiles. The system also enables restaurants to manage menu items and orders while providing administrators with complete control over the platform.

The application follows REST API principles, uses JWT authentication for security, SQLAlchemy ORM for database operations, and Pydantic for request validation.

---

# Technology Stack

- Python 3.x
- FastAPI
- MySQL
- SQLAlchemy ORM
- Pydantic
- JWT Authentication
- Passlib (bcrypt)
- Uvicorn
- Postman

---

# Project Features

- JWT Authentication
- Password Hashing using bcrypt
- Role-based Secure APIs
- CRUD Operations
- SQLAlchemy Relationships
- Pagination
- Search Restaurants
- Filter Orders by Status
- Data Validation
- Global Exception Handling
- Swagger API Documentation
- Postman API Testing

---

# Project Structure

```
online_food_delivery_system/

│── app/
│   │── main.py
│   │── database.py
│   │── config.py
│   │── models.py
│   │── schemas.py
│   │── oauth2.py
│   │── dependencies.py
│   │── utils.py
│   │── exceptions.py
│   │── middleware.py
│   │
│   ├── routers/
│   │      auth.py
│   │      users.py
│   │      restaurants.py
│   │      menu.py
│   │      orders.py
│   │      order_items.py
│   │      payments.py
│   │
│   ├── crud/
│   │      auth_crud.py
│   │      user_crud.py
│   │      restaurant_crud.py
│   │      menu_crud.py
│   │      order_crud.py
│   │      order_item_crud.py
│   │      payment_crud.py
│
│── requirements.txt
│── README.md
│── food_delivery.sql
│── Online_Food_Delivery_Postman_Collection.json
```

---

# Modules

## 1. Authentication

Features

- User Registration
- User Login
- JWT Token Generation
- Password Hashing
- Protected Routes

---

## 2. User Module

### Table

users

### APIs

- Register User
- Login User
- Get Profile
- Update Profile

---

## 3. Restaurant Module

### Table

restaurants

### APIs

- Create Restaurant
- Get All Restaurants
- Get Restaurant By ID
- Update Restaurant
- Delete Restaurant
- Search Restaurant

---

## 4. Menu Module

### Table

menu_items

### APIs

- Add Menu Item
- View Menu
- Get Menu by Restaurant
- Update Menu Item
- Delete Menu Item

---

## 5. Order Module

### Table

orders

### APIs

- Place Order
- Get All Orders
- Get Order By ID
- Update Order Status
- Cancel Order
- Filter Orders by Status

---

## 6. Order Item Module

### Table

order_items

### APIs

- Add Order Item
- Get All Order Items
- Get Order Items by Order
- Update Quantity
- Delete Order Item

---

## 7. Payment Module

### Table

payments

### APIs

- Create Payment
- Get Payment Details
- Update Payment Status

---

# Database Relationships

```
User (1)
   │
   ├───────────────< Orders (Many)

Restaurant (1)
   │
   ├───────────────< Menu Items (Many)

Restaurant (1)
   │
   ├───────────────< Orders (Many)

Order (1)
   │
   ├───────────────< Order Items (Many)

Menu Item (1)
   │
   ├───────────────< Order Items (Many)

Order (1)
   │
   └─────────────── Payment (1)
```

---

# Validations

- Valid Email Format
- Phone Number must contain 10 digits
- Password minimum 8 characters
- Restaurant Name cannot be empty
- Menu Item Name cannot be empty
- Price must be greater than 0
- Quantity must be greater than 0

---

# Authentication

This project uses **JWT (JSON Web Token)**.

### Workflow

1. Register User
2. Login
3. Receive JWT Access Token
4. Click **Authorize** in Swagger
5. Enter

```
Bearer <access_token>
```

6. Access Protected APIs

---

# API Documentation

After running the project

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Installation

## Clone Repository

```
git clone <repository_url>
```

## Create Virtual Environment

Windows

```
python -m venv venv
```

Activate

```
venv\Scripts\activate
```

---

## Install Requirements

```
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file inside the **app** folder.

Example

```
DATABASE_URL=mysql+pymysql://root:Moshika%401294@localhost:3306/food_delivery_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Create Database

```
CREATE DATABASE food_delivery_db;
```

Import

```
food_delivery.sql
```

---

## Run Project

```
uvicorn app.main:app --reload
```

---

# API Testing

The APIs can be tested using

- Swagger UI
- Postman

Import

```
Online_Food_Delivery_Postman_Collection.json
```

---

# Deliverables

- Complete FastAPI Source Code
- MySQL Database Script
- Postman Collection
- Requirements.txt
- README.md
- API Testing Screenshots
- Project ZIP / GitHub Repository

---

# Future Enhancements

- Delivery Partner Module
- Live Order Tracking
- Online Payment Gateway
- Email Notifications
- SMS Notifications
- Restaurant Ratings & Reviews
- Admin Dashboard
- Docker Deployment
- CI/CD Integration

---

# Author  : V.Deepa

**Project Title:** Online Food Delivery Management System API

**Developed Using:** FastAPI, Python, MySQL, SQLAlchemy ORM

---

# Conclusion

The Online Food Delivery Management System API is a complete backend solution for managing food ordering, restaurants, menus, orders, order items, and payments. It follows industry best practices by implementing secure JWT authentication, SQLAlchemy ORM relationships, Pydantic validation, exception handling, pagination, filtering, and RESTful API design. The project is scalable, maintainable, and suitable for learning as well as real-world backend development.
