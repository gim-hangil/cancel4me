from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Ticket(Base):
  __tablename__ = "tickets"

  id = Column(Integer, primary_key=True, autoincrement=True)
  korail_id = Column(String)
  korail_pw = Column(String)
  departure_station = Column(String)
  arrival_station = Column(String)
  date = Column(String)
  departure_base = Column(String)
  arrival_limit = Column(String)
  reserved = Column(Boolean, default=False)
