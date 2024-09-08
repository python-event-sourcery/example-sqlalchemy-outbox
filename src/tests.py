from collections.abc import Generator
from uuid import uuid4

import pytest
from starlette.testclient import TestClient

from main import app


def test_manages_item_quantity_during_ordering(client: TestClient) -> None:
    # Given an item with quantity 4
    response = client.post(
        app.url_path_for("inventory:create_item"),
        json={
            "item": "An Item",
            "quantity": 4,
        },
    )
    assert response.status_code == 201

    # And ordering 3 units of this item
    response = client.post(
        app.url_path_for("orders:create_order"),
        json={
            "order_id": uuid4().hex,
            "item_name": "An Item",
            "units": 3,
        },
    )
    assert response.status_code == 201

    # When outbox process events
    response = client.post(app.url_path_for("outbox:process"))
    assert response.status_code == 200

    # Then item quantity is 1
    response = client.get(app.url_path_for("inventory:get_quantity", item="An Item"))
    assert int(response.text) == 1


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
