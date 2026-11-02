from fastapi import Depends

from app.repository import TicketRepository
from app.service import TicketService
from app.settings import Settings, get_settings

_repository = TicketRepository()


def get_repository() -> TicketRepository:
    return _repository


def get_service(
    repository: TicketRepository = Depends(get_repository),
    settings: Settings = Depends(get_settings),
) -> TicketService:
    return TicketService(repository, settings)
