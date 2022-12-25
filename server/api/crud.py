"""CRUD functions
"""
from sqlalchemy.orm import Session

from . import model, schema


def create_ticket(db_session: Session, ticket: schema.TicketCreate):
    """Create ticket reservation record in database"""
    date = ticket.date.replace("-", "")
    departure_base = ticket.departure_base.replace(":", "") + "00"
    arrival_limit = ticket.arrival_limit.replace(":", "") + "00"
    db_ticket = model.Ticket(
        korail_id=ticket.korail_id,
        korail_pw=ticket.korail_pw,
        departure_station=ticket.departure_station,
        arrival_station=ticket.arrival_station,
        date=date,
        departure_base=departure_base,
        arrival_limit=arrival_limit,
    )
    db_session.add(db_ticket)
    db_session.commit()
    db_session.refresh(db_ticket)
    return db_ticket


def get_tickets(
    db_session: Session,
    skip: int=0,
    limit: int=100,
    date=None,
    dep=None,
    arr=None,
    dep_base=None,
    arr_limit=None,
):
    """Get ticket reservation records in DB"""
    query = db_session.query(model.Ticket)
    if date != None:
        query = query.filter(model.Ticket.date == date)
    if dep != None:
        query = query.filter(model.Ticket.dep == dep)
    if arr != None:
        query = query.filter(model.Ticket.arr == arr)
    if dep_base != None:
        query = query.filter(model.Ticket.dep_base == dep_base)
    if arr_limit != None:
        query = query.filter(model.Ticket.arr_limit == arr_limit)
    return query.order_by(model.Ticket.id).offset(skip).limit(limit).all()
