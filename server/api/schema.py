from pydantic import BaseModel


class TicketBase(BaseModel):
  departure_station: str
  arrival_station: str
  date: str
  departure_base: str
  arrival_limit: str


class TicketCreate(TicketBase):
  korail_id: str
  korail_pw: str


class Ticket(TicketBase):
  id: int
  reserved: bool

  class Config:
    orm_mode = True
