from uuid import UUID

from fastapi import APIRouter, Body

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post("/", name="orders:create_order", status_code=201)
def create_order(
    order_id: UUID = Body(...),
    item_name: str = Body(...),
    units: int = Body(...),
) -> None:
    raise NotImplementedError
