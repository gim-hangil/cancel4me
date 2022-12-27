"""FastAPI utils

Original code by dmontagu.
This code is licensed under the terms of the MIT license.
https://github.com/dmontagu/fastapi-utils/blob/d98c594b/fastapi_utils/tasks.py
"""
import asyncio
import logging
from asyncio import ensure_future
from datetime import datetime
from functools import wraps
from traceback import format_exception
from typing import Any, Callable, Coroutine, Optional, Union

from korail2 import Korail, KorailError, NeedToLoginError, TrainType
from starlette.concurrency import run_in_threadpool

from .crud import mark_ticket_reserved, mark_ticket_running
from .database import SessionLocal
from .model import Ticket


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
    print(
        "This thread will be searching for...",
        ticket.departure_station,
        ticket.arrival_station,
        ticket.date.strftime("%Y%m%d"),
        max(ticket_datetime, datetime.now()).strftime("%H%M%S"),
        TrainType.KTX,
    )
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
                    return
                except NeedToLoginError:
                    with SessionLocal() as db_session:
                        mark_ticket_running(db_session, ticket.id, False)
                        mark_ticket_reserved(db_session, ticket.id, False)
                    print(f"Failed to login - ticket #{ticket.id}!")
                    return
                except KorailError:
                    continue
