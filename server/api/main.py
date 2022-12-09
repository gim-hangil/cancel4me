"""Cancel4me API

:copyright: (c) 2022 by Hangil Gim.
:license: MIT, see LICENSE for more details.
"""
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, model, schema
from .database import SessionLocal, engine


model.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db_session():
    """Get database session"""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.get("/")
async def test():
    """Test endpoint"""
    return {
        "message": "Hello World",
    }


@app.post("/tickets", response_model=schema.Ticket)
def create_ticket(
    ticket: schema.TicketCreate,
    db_session: Session=Depends(get_db_session)
):
    """Create ticket reservation"""
    return crud.create_ticket(db_session=db_session, ticket=ticket)
