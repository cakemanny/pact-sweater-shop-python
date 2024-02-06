import pytest


@pytest.mark.asyncio
async def test_healthz(client):
    resp = await client.get("/healthz")
    assert resp.status == 200


@pytest.mark.asyncio
async def test_place_order(client, monkeypatch):
    from coldperson.knitter import Sweater, SweaterOrder

    class FakeKnitter:
        def __init__(self, *args, **kwargs) -> None:
            _ = args
            _ = kwargs
            pass

        async def get_sweater(self, order: SweaterOrder):
            return Sweater(order.colour, order.order_number)

    monkeypatch.setattr("coldperson.app.Knitter", FakeKnitter)

    resp = await client.post(
        "/bff/order",
        json={
            "colour": "white",
            "order_number": 28,
        },
    )

    assert resp.status == 200
    assert await resp.json() == {
        "colour": "white",
        "order_number": 28,
    }
