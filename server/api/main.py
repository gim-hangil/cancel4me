"""Cancel4me API

:copyright: (c) 2022 by Hangil Gim.
:license: MIT, see LICENSE for more details.
"""
from multiprocessing import Lock
from os import environ
from threading import Thread

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, model, schema
from .database import SessionLocal, engine
from .utils import repeat_every, search_trains


load_dotenv()

lock = Lock()

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=environ["CORS_ALLOW_URL"].split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


def get_db_session():
    """Get database session"""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()


@app.on_event("startup")
def start_initial_threads():
    """Create new train searching thread for the first time

    differenc between `search_tickets_periodic` is that even ticket whose
    running state is True will be start a thread.
    """
    lock.acquire()
    with SessionLocal() as db_session:
        tickets = crud.get_tickets(
            db_session=db_session,
            reserved=False,
        )
    for ticket in tickets:
        print(f"Start a searching thread - ticket #{ticket.id}")
        with SessionLocal() as db_session:
            crud.mark_ticket_running(
                db_session=db_session,
                ticket_id=ticket.id
            )
        Thread(
            target=search_trains,
            args=[ticket, ],
            daemon=True,
        ).start()
    lock.release()


@app.on_event("startup")
@repeat_every(seconds=1, wait_first=True)
def search_tickets_periodic():
    """Create new train searching thread for each of new tickets"""
    lock.acquire()
    with SessionLocal() as db_session:
        tickets = crud.get_tickets(
            db_session=db_session,
            reserved=False,
            running=False,
        )
    for ticket in tickets:
        print(f"Start a searching thread - ticket #{ticket.id}")
        with SessionLocal() as db_session:
            crud.mark_ticket_running(
                db_session=db_session,
                ticket_id=ticket.id
            )
        Thread(
            target=search_trains,
            args=[ticket, ],
            daemon=True,
        ).start()
    lock.release()


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
