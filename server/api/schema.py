"""Pydantic models

Pydantic models are used as type in FastAPI.
Since the term model is used in SQLAlchemy and means different things, used
schema instead.
"""
import datetime
from typing import Literal

from pydantic import BaseModel


class TicketBase(BaseModel):
    """Ticket schema base"""
    departure_station: str
    arrival_station: str
    date: datetime.date
    departure_base: datetime.time
    arrival_limit: datetime.time


class TicketCreate(TicketBase):
    """Ticket schema for create request"""
    korail_id: str
    korail_pw: str
    phone_number: str


class TicketRead(TicketBase):
    """Ticket schema for read request"""
    id: int
    reserved: bool
    running: bool

    class Config:
        """Configuration for ORM support"""
        orm_mode = True


class JSendModel(BaseModel):
    """JSend format base model"""
    status: Literal["success", "fail", "error"]
    data: dict


class TicketJSend(JSendModel):
    """Ticket response model in JSend format"""
    data: TicketRead

class TicketsJSend(JSendModel):
    """Array of tickets response model in JSend format"""
    data: list[TicketRead]
