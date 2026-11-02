"""Стартовый код сервиса тикетов техподдержки.

Часть классов и функций уже реализована, часть содержит TODO.
Структура данных тикета и правила перехода статуса заданы ниже.
Логику репозитория, сервиса и части эндпоинтов нужно доделать.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .routes import tikets

from app.exceptions import InvalidStatusTransitionError, TicketNotFoundError

app = FastAPI(title="HelpDesk Lite")
app.include_router(tikets.router)

@app.exception_handler(TicketNotFoundError)
def handle_not_found(request: Request, exc: TicketNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(InvalidStatusTransitionError)
def handle_invalid_transition(request: Request, exc: InvalidStatusTransitionError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


