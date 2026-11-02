from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from ..schemas import Ticket, TicketCreate, TicketListParams, TicketPage, TicketUpdate
from ..service import TicketService
from ..dependencies import get_service

router = APIRouter(prefix="/tikets", tags=["Тикеты тех поддержки"])

@router.post(
    path="/",
    response_model=Ticket,
    status_code=status.HTTP_201_CREATED,
    summary="Создать тикет",
)
def create_ticket(payload: TicketCreate, service: TicketService = Depends(get_service)):
    return service.create_ticket(payload)


@router.get(
    path="/",
    response_model=TicketPage,
    summary="Получить список тикетов",
)
def list_tickets(
    params: Annotated[TicketListParams, Query()],
    service: TicketService = Depends(get_service),
):
    return service.list_tickets(params)


@router.get(
    "/{ticket_id}",
    response_model=Ticket,
    summary="Получить тикет по id",
)
def get_ticket(ticket_id: int, service: TicketService = Depends(get_service)):
    return service.get_ticket(ticket_id)


@router.patch(
    "/{ticket_id}",
    response_model=Ticket,
    summary="Изменить часть данных тикета",
)
def update_ticket(
    ticket_id: int,
    changes: TicketUpdate,
    service: TicketService = Depends(get_service),
):
    return service.update_ticket(ticket_id, changes)


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить тикет",
)
def delete_ticket(ticket_id: int, service: TicketService = Depends(get_service)):
    service.delete_ticket(ticket_id)
