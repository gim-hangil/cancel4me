"""FastAPI utils

Original code by dmontagu.
This code is licensed under the terms of the MIT license.
https://github.com/dmontagu/fastapi-utils/blob/d98c594b/fastapi_utils/tasks.py
"""
import asyncio
import logging
from asyncio import ensure_future
from base64 import b64encode
from datetime import datetime
from dotenv import load_dotenv
from hashlib import sha256
from hmac import new as new_hmac
from functools import wraps
from os import environ
from time import time
from traceback import format_exception
from typing import Any, Callable, Coroutine, Optional, Union

from korail2 import Korail, KorailError, NeedToLoginError, NoResultsError, TrainType
from requests import request
from starlette.concurrency import run_in_threadpool

from .crud import mark_ticket_reserved, mark_ticket_running
from .database import SessionLocal
from .model import Ticket


load_dotenv()


NoArgsNoReturnFuncT = Callable[[], None]
NoArgsNoReturnAsyncFuncT = Callable[[], Coroutine[Any, Any, None]]
NoArgsNoReturnDecorator = Callable[
    [Union[NoArgsNoReturnFuncT, NoArgsNoReturnAsyncFuncT]],
    NoArgsNoReturnAsyncFuncT
]


def repeat_every(
    *,
    seconds: float,
    wait_first: bool = False,
    logger: Optional[logging.Logger] = None,
    raise_exceptions: bool = False,
    max_repetitions: Optional[int] = None,
) -> NoArgsNoReturnDecorator:
    """
    This function returns a decorator that modifies a function so it is
    periodically re-executed after its first call.
    The function it decorates should accept no arguments and return nothing. If
    necessary, this can be accomplished
    by using `functools.partial` or otherwise wrapping the target function prior
    to decoration.

    Parameters
    ----------
    seconds: float
        The number of seconds to wait between repeated calls
    wait_first: bool (default False)
        If True, the function will wait for a single period before the first
        call
    logger: Optional[logging.Logger] (default None)
        The logger to use to log any exceptions raised by calls to the decorated
        function.
        If not provided, exceptions will not be logged by this function (though
        they may be handled by the event loop).
    raise_exceptions: bool (default False)
        If True, errors raised by the decorated function will be raised to the
        event loop's exception handler.
        Note that if an error is raised, the repeated execution will stop.
        Otherwise, exceptions are just logged and the execution continues to
        repeat.
        See document below for more info.
        https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.set_exception_handler
    max_repetitions: Optional[int] (default None)
        The maximum number of times to call the repeated function. If `None`,
        the function is repeated forever.
    """

    def decorator(
        func: Union[NoArgsNoReturnAsyncFuncT, NoArgsNoReturnFuncT]
    ) -> NoArgsNoReturnAsyncFuncT:
        """
        Converts the decorated function into a repeated, periodically-called
        version of itself.
        """
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapped() -> None:
            repetitions = 0

            async def loop() -> None:
                nonlocal repetitions
                if wait_first:
                    await asyncio.sleep(seconds)
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        if is_coroutine:
                            await func()    # type: ignore
                        else:
                            await run_in_threadpool(func)
                        repetitions += 1
                    # pylint: disable=broad-except
                    except Exception as exc:
                        if logger is not None:
                            formatted_exception = "".join(
                                format_exception(
                                type(exc), exc, exc.__traceback__
                                )
                            )
                            logger.error(formatted_exception)
                        if raise_exceptions:
                            raise exc
                    await asyncio.sleep(seconds)

            ensure_future(loop())

        return wrapped

    return decorator


def search_trains(ticket: Ticket):
    """Search for available tickets"""
    with SessionLocal() as db_session:
        mark_ticket_running(db_session, ticket.id)
    korail = Korail(ticket.korail_id, ticket.korail_pw)
    ticket_datetime = datetime.combine(ticket.date, ticket.departure_base)
    while ticket_datetime > datetime.now():
        trains = korail.search_train_allday(
            dep=ticket.departure_station,
            arr=ticket.arrival_station,
            date=ticket.date.strftime("%Y%m%d"),
            time=max(ticket_datetime, datetime.now()).strftime("%H%M%S"),
            train_type=TrainType.KTX,
        )
        for train in trains:
            if (
                train.dep_name == ticket.departure_station and
                train.arr_name == ticket.arrival_station and
                train.dep_date == ticket.date.strftime("%Y%m%d") and
                train.dep_time > ticket.departure_base.strftime("%H%M%S") and
                train.arr_time < ticket.arrival_limit.strftime("%H%M%S")
            ):
                try:
                    korail.reserve(train)
                    with SessionLocal() as db_session:
                        mark_ticket_reserved(db_session, ticket.id)
                        mark_ticket_running(db_session, ticket.id, False)
                    print(f"Made a reservation - ticket #{ticket.id}!")
                    print(send_notification(
                        msg="예약이 완료되었습니다. 코레일에서 결제하세요.",
                        send_from=environ["SENS_SEND_FROM"].replace("-", ""),
                        send_to=ticket.phone_number.replace("-", ""),
                        service_id=environ["SENS_SERVICE_ID"],
                        access_key=environ["NCP_ACCESS_KEY"],
                        secret_key=environ["NCP_SECRET_KEY"],
                    ))
                    return
                except NeedToLoginError:
                    with SessionLocal() as db_session:
                        mark_ticket_running(db_session, ticket.id, False)
                        mark_ticket_reserved(db_session, ticket.id, False)
                    print(f"Failed to login - ticket #{ticket.id}!")
                    return
                except NoResultsError:
                    print(f"No result - ticket #{ticket.id}")
                except KorailError:
                    continue


def make_ncp_signature(method, uri, timestamp, access_key, secret_key):
    """Make NCP signature for SENS API"""
    message = f"{method} {uri}\n{timestamp}\n{access_key}"
    message = bytes(message, "UTF-8")
    secret_key = bytes(secret_key, "UTF-8")
    signing_key = b64encode(new_hmac(secret_key, message, digestmod=sha256).digest())
    return signing_key


def send_notification(msg, send_from, send_to, service_id, access_key, secret_key):
    """Sends SMS using NCP SENS API"""
    sens_url = "https://sens.apigw.ntruss.com"
    sens_sms_path = f"/sms/v2/services/{service_id}/messages"
    sens_sms_url = f"{sens_url}{sens_sms_path}"

    timestamp = str(int(time() * 1000))
    signature = make_ncp_signature(
        method="POST",
        uri=sens_sms_path,
        timestamp=timestamp,
        access_key=access_key,
        secret_key=secret_key,
    )

    notify_response = request(
        method="POST",
        url=sens_sms_url,
        headers={
            "Content-Type": "application/json; charset=UTF-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signature,
        },
        json={
            "type": "SMS",
            "from": send_from,
            "content": msg,
            "messages": [
                {
                    "to": send_to,
                },
            ],
        },
        timeout=5,
    )

    return notify_response.json()
