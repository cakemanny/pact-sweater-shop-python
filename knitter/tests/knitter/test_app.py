import json

import pytest
import pytest_asyncio


@pytest_asyncio.fixture
async def client(aiohttp_client):
    from knitter.app import make_app

    app = make_app()
    client = await aiohttp_client(app)
    return client


@pytest.mark.asyncio
async def test_healthz(client):
    resp = await client.get("/healthz")
    assert resp.status == 200


@pytest.mark.asyncio
async def test_knit_sweater(client):
    # TODO: create a pact with the farmer and use it as a mock

    resp = await client.post(
        "/sweater/order",
        data=json.dumps(
            {
                "colour": "white",
                "order_number": 142,
            }
        ),
    )
    assert resp.status == 200
    assert await resp.json() == {
        "colour": "white",
        "order_number": 142,
        "style": "long_sleeved",
    }
