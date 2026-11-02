from app.exceptions import InvalidStatusTransitionError, TicketNotFoundError
from app.repository import TicketRepository
from app.schemas import (
    ALLOWED_TRANSITIONS,
    Priority,
    SortOrder,
    Ticket,
    TicketCreate,
    TicketListParams,
    TicketPage,
    TicketSortBy,
    TicketUpdate,
)
from app.settings import Settings


class TicketService:
    def __init__(self, repository: TicketRepository, settings: Settings) -> None:
        self._repository = repository
        self._settings = settings

    def create_ticket(self, payload: TicketCreate) -> Ticket:
        new_id = self._repository.next_id()
        new_ticket = Ticket(id=new_id, **payload.model_dump())
        self._repository.add(new_ticket)
        return new_ticket

    def get_ticket(self, ticket_id: int) -> Ticket:
        ticket = self._repository.get(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)
        return ticket

    def list_tickets(self, params: TicketListParams) -> TicketPage:
        page_size = (
            params.page_size
            if params.page_size is not None
            else self._settings.default_page_size
        )
        page_size = min(page_size, self._settings.max_page_size)

        tickets = self._repository.list_all()
        total = len(tickets)

        priority_order = {priority: rank for rank, priority in enumerate(Priority)}

        if params.sort_by is TicketSortBy.created_at:
            sort_key = lambda ticket: ticket.created_at
        else:
            sort_key = lambda ticket: priority_order[ticket.priority]

        tickets.sort(key=sort_key, reverse=params.order is SortOrder.desc)

        start = (params.page - 1) * page_size
        items = tickets[start : start + page_size]

        return TicketPage(
            items=items,
            total=total,
            page=params.page,
            page_size=page_size,
        )

    def update_ticket(self, ticket_id: int, changes: TicketUpdate) -> Ticket:
        ticket = self._repository.get(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)
        if changes.status and changes.status not in ALLOWED_TRANSITIONS.get(ticket.status, set()):
            raise InvalidStatusTransitionError(ticket.status, changes.status)
        updated_ticket = ticket.model_copy(update=changes.model_dump(exclude_none=True))
        self._repository.update(updated_ticket)
        return updated_ticket

    def delete_ticket(self, ticket_id: int) -> None:
        if not self._repository.delete(ticket_id):
            raise TicketNotFoundError(ticket_id)
        
