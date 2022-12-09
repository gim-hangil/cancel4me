"""Pydantic models

Since the term model is used in SQLAlchemy and means different things, used
schema instead.
"""
from pydantic import BaseModel


class TicketBase(BaseModel):
    """Ticket schema base"""
    departure_station: str
    arrival_station: str
    date: str
    departure_base: str
    arrival_limit: str


class TicketCreate(TicketBase):
    """Ticket schema for create request"""
    korail_id: str
    korail_pw: str


class Ticket(TicketBase):
    """Ticket schema for read request"""
    id: int
    reserved: bool

    class Config:
        """Configuration for ORM support"""
        orm_mode = True
