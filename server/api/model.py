"""SQLAlchemy models
"""
from sqlalchemy import Boolean, Column, Integer, String, Date, Time

from .database import Base


class Ticket(Base):
    """Ticket model

    The tickets that user requested to reserve. Workers will read requests from
    this table on startup and periodically search for cancelled tickets.
    """
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    korail_id = Column(String)
    korail_pw = Column(String)
    departure_station = Column(String)
    arrival_station = Column(String)
    date = Column(Date)
    departure_base = Column(Time)
    arrival_limit = Column(Time)
    reserved = Column(Boolean, default=False)
    running = Column(Boolean, default=False)
