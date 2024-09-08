from uuid import UUID

from event_sourcery.event_store import Backend, Event, StreamId
from fastapi import APIRouter, Body, Depends

from backend import backend

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


class OrderPlaced(Event):
    item: str
    units: int


@router.post("/", name="orders:create_order", status_code=201)
def create_order(
    order_id: UUID = Body(...),
    item_name: str = Body(...),
    units: int = Body(...),
    backend: Backend = Depends(backend),
) -> None:
    backend.event_store.append(
        OrderPlaced(item=item_name, units=units),
        stream_id=StreamId(order_id, category="orders"),
    )
