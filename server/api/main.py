"""Cancel4me API

:copyright: (c) 2022 by Hangil Gim.
:license: MIT, see LICENSE for more details.
"""
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from korail2 import Korail
from os import environ
from sqlalchemy.orm import Session

from . import crud, model, schema
from .database import SessionLocal, engine
from .utils import repeat_every


load_dotenv()

model.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=environ["CORS_ALLOW_URL"].split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

korail = Korail("", "", auto_login=False)


def get_db_session():
    """Get database session"""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.on_event("startup")
@repeat_every(seconds=1)
def search_tickets():
    global korail
    try:
        trains = korail.search_train_allday(dep="서울", arr="부산", time="000000")
        print(trains[0])
    except Exception as e:
        print(e)


@app.get("/")
async def test():
    """Test endpoint"""
    return {
        "message": "Hello World",
    }


@app.get("/tickets", response_model=schema.TicketsJSend)
def get_tickets(
    skip: int=0,
    limit: int=100,
    db_session: Session=Depends(get_db_session),
):
    """Get ticket reservations"""
    return {
        "status": "success",
        "data": crud.get_tickets(db_session=db_session, skip=skip, limit=limit)
    }


@app.post("/tickets", response_model=schema.TicketJSend)
def create_ticket(
    ticket: schema.TicketCreate,
    db_session: Session=Depends(get_db_session)
):
    """Create ticket reservation"""
    return {
        "status": "success",
        "data": crud.create_ticket(db_session=db_session, ticket=ticket),
    }
