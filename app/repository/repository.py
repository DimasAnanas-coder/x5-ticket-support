from app.schemas import Ticket


class TicketRepository:
    """Хранит тикеты в памяти процесса."""

    def __init__(self) -> None:
        self._tickets: dict[int, Ticket] = {}
        self._next_id = 1

    def add(self, ticket: Ticket) -> Ticket:
        self._tickets[ticket.id] = ticket
        return self._tickets[ticket.id]

    def get(self, ticket_id: int) -> Ticket:
        return self._tickets.get(ticket_id)

    def list_all(self) -> list[Ticket]:
        return list(self._tickets.values())

    def update(self, ticket: Ticket) -> Ticket:
        self._tickets[ticket.id] = ticket
        return ticket

    def delete(self, ticket_id: int) -> None:
        return self._tickets.pop(ticket_id, None)

    def next_id(self) -> int:
        ticket_id = self._next_id
        self._next_id += 1
        return ticket_id
