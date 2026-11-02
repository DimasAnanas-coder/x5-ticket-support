"""Стартовый код сервиса тикетов техподдержки.

Часть классов и функций уже реализована, часть содержит TODO.
Структура данных тикета и правила перехода статуса заданы ниже.
Логику репозитория, сервиса и части эндпоинтов нужно доделать.
"""

from fastapi import Depends, FastAPI, Query, Request, status
from fastapi.responses import JSONResponse

from app.dependencies import get_service
from app.exceptions import InvalidStatusTransitionError, TicketNotFoundError
from app.schemas import Ticket, TicketCreate, TicketPage, TicketUpdate
from app.service import TicketService

app = FastAPI(title="HelpDesk Lite")


@app.exception_handler(TicketNotFoundError)
def handle_not_found(request: Request, exc: TicketNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(InvalidStatusTransitionError)
def handle_invalid_transition(request: Request, exc: InvalidStatusTransitionError) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})


@app.post(
    "/tickets",
    response_model=Ticket,
    status_code=status.HTTP_201_CREATED,
    tags=["tickets"],
    summary="Создать тикет",
)
def create_ticket(payload: TicketCreate, service: TicketService = Depends(get_service)):
    return service.create_ticket(payload)


@app.get(
    "/tickets",
    response_model=TicketPage,
    tags=["tickets"],
    summary="Получить список тикетов",
)
def list_tickets(
    sort_by: str = Query("created_at", pattern="^(created_at|priority)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int | None = Query(None, ge=1),
    service: TicketService = Depends(get_service),
):
    raise NotImplementedError


@app.get(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    tags=["tickets"],
    summary="Получить тикет по id",
    
)
def get_ticket(ticket_id: int, service: TicketService = Depends(get_service)):
    return service.get_ticket(ticket_id)


@app.patch(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    tags=["tickets"],
    summary="Изменить часть данных тикета",
)
def update_ticket(
    ticket_id: int,
    changes: TicketUpdate,
    service: TicketService = Depends(get_service),
):
    return service.update_ticket(ticket_id, changes)


@app.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tickets"],
    summary="Удалить тикет",
)
def delete_ticket(ticket_id: int, service: TicketService = Depends(get_service)):
    service.delete_ticket(ticket_id)
