from app.exceptions import InvalidStatusTransitionError, TicketNotFoundError
from app.repository import TicketRepository
from app.schemas import ALLOWED_TRANSITIONS, Ticket, TicketCreate, TicketPage, TicketUpdate
from app.settings import Settings


class TicketService:
    def __init__(self, repository: TicketRepository, settings: Settings) -> None:
        self._repository = repository
        self._settings = settings

    def create_ticket(self, payload: TicketCreate) -> Ticket:
        new_id = self.repository.next_id()
        new_ticket = Ticket(id=new_id, **payload.model_dump())
        self._repository.add(new_ticket)
        return new_ticket

    def get_ticket(self, ticket_id: int) -> Ticket:
        ticket = self._repository.get(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)
        return ticket

    def list_tickets(
        self,
        sort_by: str,
        order: str,
        page: int,
        page_size: int | None,
    ) -> TicketPage:
        # TODO: применить page_size из settings, если не передан,
        #  ограничить его settings.max_page_size, отсортировать список
        #  и вернуть нужную страницу
        raise NotImplementedError

    def update_ticket(self, ticket_id: int, changes: TicketUpdate) -> Ticket:
        ticket = self._repository.get(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)
        if ALLOWED_TRANSITIONS[ticket.status] != changes.status:
            raise InvalidStatusTransitionError(ticket.status, changes.status)
        updated_ticket = ticket.model_copy(update=changes.model_dump())
        self._repository.update(updated_ticket)
        return updated_ticket

    def delete_ticket(self, ticket_id: int) -> None:
        if not self._repository.delete(ticket_id):
            raise TicketNotFoundError(ticket_id)
        
