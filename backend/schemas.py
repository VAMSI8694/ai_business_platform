from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime

# Auth Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Agent Schemas
class AgentRequest(BaseModel):
    message: str
    agent_name: str
    session_id: Optional[str] = None
    context: Optional[dict] = None

class AgentResponse(BaseModel):
    response: str
    agent_name: str
    session_id: str
    tokens_used: int
    success: bool

# Business Data Schemas
class AccountCreate(BaseModel):
    account_name: str
    account_type: str
    balance: float
    currency: str = "USD"

class SaleCreate(BaseModel):
    customer_name: str
    product_name: str
    quantity: int
    unit_price: float

class PurchaseOrderCreate(BaseModel):
    supplier_name: str
    item_name: str
    quantity: int
    unit_price: float

class ManufacturingOrderCreate(BaseModel):
    product_name: str
    quantity: int
    start_date: str
    end_date: str
    cost: float

class InvestmentCreate(BaseModel):
    investment_name: str
    investment_type: str
    amount: float
    return_rate: float
    start_date: str
