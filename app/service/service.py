from app.exceptions import InvalidStatusTransitionError
from app.repository import TicketRepository
from app.schemas import ALLOWED_TRANSITIONS, Ticket, TicketCreate, TicketPage, TicketUpdate
from app.settings import Settings


class TicketService:
    def __init__(self, repository: TicketRepository, settings: Settings) -> None:
        self._repository = repository
        self._settings = settings

    def create_ticket(self, payload: TicketCreate) -> Ticket:
        raise NotImplementedError

    def get_ticket(self, ticket_id: int) -> Ticket:
        return self._repository.get(ticket_id)

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
        # TODO: применить изменения, при смене статуса проверить
        # ALLOWED_TRANSITIONS и поднять InvalidStatusTransitionError
        raise NotImplementedError

    def delete_ticket(self, ticket_id: int) -> None:
        self._repository.delete(ticket_id)
