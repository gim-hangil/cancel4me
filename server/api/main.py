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


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.get("/")
async def test():
  return {
    "message": "Hello World",
  }


@app.post("/tickets", response_model=schema.Ticket)
def create_ticket(ticket: schema.TicketCreate, db: Session=Depends(get_db)):
  return crud.create_ticket(db=db, ticket=ticket)
