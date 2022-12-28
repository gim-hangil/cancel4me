"""CRUD functions
"""
from datetime import datetime

from sqlalchemy.orm import Session

from . import model, schema


def create_ticket(db_session: Session, ticket: schema.TicketCreate):
    """Create ticket reservation record in database"""
    db_ticket = model.Ticket(
        phone_number=ticket.phone_number,
        korail_id=ticket.korail_id,
        korail_pw=ticket.korail_pw,
        departure_station=ticket.departure_station,
        arrival_station=ticket.arrival_station,
        date=ticket.date,
        departure_base=ticket.departure_base,
        arrival_limit=ticket.arrival_limit,
    )
    db_session.add(db_ticket)
    db_session.commit()
    db_session.refresh(db_ticket)
    return db_ticket


def get_tickets(
    db_session: Session,
    skip: int=0,
    limit: int=100,
    after_now: bool=False,
    reserved: bool=None,
    running: bool=None,
) -> list[model.Ticket]:
    """Get ticket reservation records in DB"""
    query = db_session.query(model.Ticket)
    if after_now:
        query = query.filter(
            (model.Ticket.date > datetime.now().date()) |
            (
                (model.Ticket.date == datetime.now().date()) &
                (model.Ticket.departure_base > datetime.now().time())
            )
        )
    if reserved is not None:
        query = query.filter(model.Ticket.reserved == reserved)
    if running is not None:
        query = query.filter(model.Ticket.running == running)
    return query.order_by(model.Ticket.id).offset(skip).limit(limit).all()


def mark_ticket_reserved(
    db_session: Session,
    ticket_id: int,
    reserved: bool=True
):
    """Update ticket.reserved as true"""
    query = db_session.query(model.Ticket).filter(model.Ticket.id == ticket_id)
    query.update({ "reserved": reserved })
    db_session.commit()

def mark_ticket_running(
    db_session: Session,
    ticket_id: int,
    running: bool=True
):
    """Update ticket.running as False"""
    query = db_session.query(model.Ticket).filter(model.Ticket.id == ticket_id)
    query.update({ "running": running })
    db_session.commit()
