from app.schemas import TicketStatus


class HelpDeskError(Exception):
    """Базовое исключение сервиса."""


class TicketNotFoundError(HelpDeskError):
    def __init__(self, ticket_id: int) -> None:
        self.ticket_id = ticket_id
        super().__init__(f"Тикет {ticket_id} не найден")


class InvalidStatusTransitionError(HelpDeskError):
    def __init__(self, current: TicketStatus, target: TicketStatus) -> None:
        self.current = current
        self.target = target
        super().__init__(f"Переход {current} -> {target} запрещён")
