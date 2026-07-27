from datetime import datetime
from decimal import Decimal
from typing import Optional
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# =====================================================
# JWT TOKEN SCHEMAS
# =====================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# =====================================================
# USER SCHEMAS
# =====================================================

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r"^[0-9]{10}$")
    address: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, max_length=100)
    phone: Optional[str] = Field(None, pattern=r"^[0-9]{10}$")
    address: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# RESTAURANT SCHEMAS
# =====================================================

class RestaurantBase(BaseModel):
    restaurant_name: str = Field(..., min_length=1, max_length=150)
    owner_name: str = Field(..., min_length=3, max_length=100)
    phone: str = Field(..., pattern=r"^[0-9]{10}$")
    email: EmailStr
    address: str
    status: Optional[str] = "OPEN"


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    restaurant_name: Optional[str] = None
    owner_name: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r"^[0-9]{10}$")
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    status: Optional[str] = None


class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# MENU ITEM SCHEMAS
# =====================================================

class MenuItemBase(BaseModel):
    restaurant_id: int
    item_name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    category: Optional[str] = None
    availability: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    item_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = None
    availability: Optional[bool] = None


class MenuItemResponse(MenuItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# ORDER SCHEMAS
# =====================================================

class OrderBase(BaseModel):
    user_id: int
    restaurant_id: int
    total_amount: Decimal = Field(..., gt=0)
    order_status: Optional[str] = "PENDING"


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    order_status: str


class OrderResponse(OrderBase):
    id: int
    order_date: datetime

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# ORDER ITEM SCHEMAS
# =====================================================

class OrderItemBase(BaseModel):
    order_id: int
    menu_item_id: int
    quantity: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    menu_item_id: int
    quantity: int
    price: Decimal

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# PAYMENT SCHEMAS
# =====================================================

class PaymentBase(BaseModel):
    order_id: int
    payment_method: str
    


class PaymentStatus(str, Enum):
    pending = "PENDING"
    success = "SUCCESS"
    failed = "FAILED"

class PaymentStatusUpdate(BaseModel):
    payment_status: PaymentStatus

class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    payment_status: str


class PaymentResponse(PaymentBase):
    id: int
    order_id: int
    payment_method: str
    payment_status: str
    transaction_id: str
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)

    # =====================================================
    # ORDER SCHEMAS
    # =====================================================

class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    restaurant_id: int
    items: list[OrderItemRequest]


class OrderStatusUpdate(BaseModel):
    order_status: str


class OrderResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    total_amount: Decimal
    order_status: str
    order_date: datetime

    model_config = ConfigDict(from_attributes=True)