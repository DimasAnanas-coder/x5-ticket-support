from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class TicketSortBy(str, Enum):
    created_at = "created_at"
    priority = "priority"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


ALLOWED_TRANSITIONS: dict[TicketStatus, set[TicketStatus]] = {
    TicketStatus.open: {TicketStatus.in_progress},
    TicketStatus.in_progress: {TicketStatus.resolved, TicketStatus.open},
    TicketStatus.resolved: {TicketStatus.closed, TicketStatus.in_progress},
    TicketStatus.closed: set(),
}


class TicketCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str | None = None
    priority: Priority = Priority.normal
    assignee: str | None = None


class TicketUpdate(BaseModel):
    description: str | None = None
    priority: Priority | None = None
    assignee: str | None = None
    status: TicketStatus | None = None


class Ticket(BaseModel):
    id: int
    title: str
    description: str | None
    priority: Priority
    status: TicketStatus = Field(default=TicketStatus.open)
    assignee: str | None
    created_at: datetime = Field(default_factory=datetime.now)


class TicketPage(BaseModel):
    items: list[Ticket]
    total: int
    page: int
    page_size: int


class TicketListParams(BaseModel):
    sort_by: TicketSortBy = TicketSortBy.created_at
    order: SortOrder = SortOrder.desc
    page: int = Field(default=1, ge=1)
    page_size: int | None = Field(default=None, ge=1)
