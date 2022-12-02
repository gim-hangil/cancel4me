"""Cancel4me API

:copyright: (c) 2022 by Hangil Gim.
:license: MIT, see LICENSE for more details.
"""
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def test():
  return {
    "message": "Hello World",
  }