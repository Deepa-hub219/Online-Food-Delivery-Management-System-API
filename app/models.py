from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DECIMAL,
    Boolean,
    ForeignKey,
    DateTime,
    Enum
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


# ==========================================
# USER MODEL
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(10), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    orders = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ==========================================
# RESTAURANT MODEL
# ==========================================

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(150), nullable=False, index=True)
    owner_name = Column(String(100), nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    address = Column(Text, nullable=False)

    status = Column(
        Enum("OPEN", "CLOSED", "INACTIVE", name="restaurant_status"),
        default="OPEN"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    menu_items = relationship(
        "MenuItem",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )

    orders = relationship(
        "Order",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )


# ==========================================
# MENU ITEM MODEL
# ==========================================

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False
    )

    item_name = Column(String(150), nullable=False)
    description = Column(Text)

    price = Column(DECIMAL(10, 2), nullable=False)

    category = Column(String(100))

    availability = Column(Boolean, default=True)

    restaurant = relationship(
        "Restaurant",
        back_populates="menu_items"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="menu_item",
        cascade="all, delete-orphan"
    )


# ==========================================
# ORDER MODEL
# ==========================================

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False
    )

    total_amount = Column(DECIMAL(10, 2), nullable=False)

    order_status = Column(
        Enum(
            "PENDING",
            "CONFIRMED",
            "PREPARING",
            "OUT_FOR_DELIVERY",
            "DELIVERED",
            "CANCELLED",
            name="order_status"
        ),
        default="PENDING"
    )

    order_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="orders"
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="orders"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    payment = relationship(
        "Payment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan"
    )


# ==========================================
# ORDER ITEM MODEL
# ==========================================

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )

    menu_item_id = Column(
        Integer,
        ForeignKey("menu_items.id", ondelete="CASCADE"),
        nullable=False
    )

    quantity = Column(Integer, nullable=False)

    price = Column(DECIMAL(10, 2), nullable=False)

    order = relationship(
        "Order",
        back_populates="order_items"
    )

    menu_item = relationship(
        "MenuItem",
        back_populates="order_items"
    )


# ==========================================
# PAYMENT MODEL
# ==========================================

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    payment_method = Column(
        Enum(
            "UPI",
            "CARD",
            "NET_BANKING",
            "CASH_ON_DELIVERY",
            name="payment_method"
        ),
        nullable=False
    )

    payment_status = Column(
        Enum(
            "PENDING",
            "SUCCESS",
            "FAILED",
            name="payment_status"
        ),
        default="PENDING"
    )

    transaction_id = Column(
        String(255),
        unique=True
    )

    payment_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    order = relationship(
        "Order",
        back_populates="payment"
    )