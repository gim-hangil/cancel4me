"""CRUD functions
"""
from sqlalchemy.orm import Session

from . import model, schema


def create_ticket(db: Session, ticket: schema.TicketCreate):
  db_ticket = model.Ticket(
    korail_id=ticket.korail_id,
    korail_pw=ticket.korail_pw,
    departure_station=ticket.departure_station,
    arrival_station=ticket.arrival_station,
    date=ticket.date,
    departure_base=ticket.departure_base,
    arrival_limit=ticket.arrival_limit,
  )
  db.add(db_ticket)
  db.commit()
  db.refresh(db_ticket)
  return db_ticket


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
  return db.query(model.Ticket).offset(skip).limit(limit).all()
