from collections.abc import Generator
from dataclasses import dataclass
from typing import ClassVar

from event_sourcery.aggregate import Aggregate, Repository
from event_sourcery.event_store import (
    Backend,
    Event,
    StreamUUID,
)
from fastapi import APIRouter, Body, Depends

from backend import backend


@dataclass
class Quantity(Aggregate):
    category: ClassVar[str] = "quantity"
    quantity: int = 0

    class Adjust(Event):
        quantity: int

    def adjust(self, by: int) -> None:
        self._emit(self.Adjust(quantity=self.quantity + by))

    def __apply__(self, event: Event) -> None:
        if type(event) is Quantity.Adjust:
            self.quantity = event.quantity


class QuantityRepository(Repository[Quantity]):
    pass


def quantity_repository(
    backend: Backend = Depends(backend),
) -> Generator[QuantityRepository, None, None]:
    yield QuantityRepository(backend.event_store)


router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)


@router.post(
    "/",
    name="inventory:create_item",
    status_code=201,
)
def create_item(
    item: str = Body(...),
    quantity: int = Body(...),
    repository: QuantityRepository = Depends(quantity_repository),
) -> None:
    with repository.aggregate(StreamUUID(name=item), Quantity()) as aggregate:
        aggregate.adjust(by=quantity)
