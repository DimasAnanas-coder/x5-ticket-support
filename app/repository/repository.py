from app.exceptions import TicketNotFoundError
from app.schemas import Ticket


class TicketRepository:
    """Хранит тикеты в памяти процесса."""

    def __init__(self) -> None:
        self._tickets: dict[int, Ticket] = {}
        self._next_id = 1

    def add(self, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    def get(self, ticket_id: int) -> Ticket:
        ticket = self._tickets.get(ticket_id)
        if not ticket:
            raise TicketNotFoundError(ticket_id)
        return ticket

    def list_all(self) -> list[Ticket]:
        raise NotImplementedError

    def update(self, ticket: Ticket) -> Ticket:
        raise NotImplementedError

    def delete(self, ticket_id: int) -> None:
        # TODO: удалить тикет или поднять TicketNotFoundError
        raise NotImplementedError

    def next_id(self) -> int:
        ticket_id = self._next_id
        self._next_id += 1
        return ticket_id
