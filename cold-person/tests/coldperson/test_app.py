import json

import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def client(aiohttp_client):
    from coldperson.app import make_app

    app = make_app()
    client = await aiohttp_client(app)
    return client


@pytest.mark.asyncio
async def test_healthz(client):
    resp = await client.get("/healthz")
    assert resp.status == 200


@pytest.mark.asyncio
async def test_place_order(client, monkeypatch):
    from coldperson.knitter import Sweater, SweaterOrder

    class FakeKnitter:
        def __init__(self, *args, **kwargs) -> None:
            pass

        async def get_sweater(self, order: SweaterOrder):
            return Sweater(order.colour, order.order_number)

    monkeypatch.setattr('coldperson.app.Knitter', FakeKnitter)

    resp = await client.post("/bff/order", data=json.dumps({
        "colour": "white",
        "order_number": 28,
    }))

    assert resp.status == 200
    assert await resp.json() == {
        "colour": "white",
        "order_number": 28,
    }
