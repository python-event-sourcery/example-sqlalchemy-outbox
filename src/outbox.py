from collections.abc import Callable

from event_sourcery.event_store import (
    Backend,
    Metadata,
    Position,
    StreamId,
)
from fastapi import APIRouter, Depends

from backend import backend
from inventory import QuantityRepository, quantity_repository

type Listener = Callable[[Metadata, StreamId, Position], None]

router = APIRouter(
    prefix="/outbox",
    tags=["outbox"],
)


@router.post("/process", name="outbox:process", status_code=200)
def process(
    pyes_backend: Backend = Depends(backend),
    inventory: QuantityRepository = Depends(quantity_repository),
) -> None:
    pyes_backend.outbox.run(inventory.publish)
