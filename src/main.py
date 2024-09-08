from fastapi import FastAPI

import inventory
import ordering
import outbox

app = FastAPI()
app.include_router(inventory.router)
app.include_router(ordering.router)
app.include_router(outbox.router)
