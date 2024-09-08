from fastapi import APIRouter

router = APIRouter(
    prefix="/outbox",
    tags=["outbox"],
)


@router.post("/process", name="outbox:process", status_code=200)
def process() -> None:
    raise NotImplementedError
